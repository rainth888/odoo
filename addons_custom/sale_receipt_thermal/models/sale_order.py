# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    receipt_number = fields.Char(string='收据号', compute='_compute_receipt_voucher_numbers')
    voucher_number = fields.Char(string='传票号', compute='_compute_receipt_voucher_numbers')

    @api.depends('invoice_ids', 'invoice_ids.state', 'invoice_ids.line_ids.matched_debit_ids', 'invoice_ids.line_ids.matched_credit_ids')
    def _compute_receipt_voucher_numbers(self):
        for order in self:
            receipt_names = set()
            voucher_names = []

            invoices = order.invoice_ids.filtered(lambda m: m.state == 'posted')
            for inv in invoices:
                # 传票号：直接取发票/凭证号
                if inv.name:
                    voucher_names.append(inv.name)

                # 收据号：取与发票对账的付款单（或相关分录）的编号
                # 从应收/应付分录出发，沿部分核销记录找到对方分录，再反查其来源付款/分录编号
                def _is_receivable_payable(l):
                    account = l.account_id
                    if not account:
                        return False
                    # Odoo 14-16: account.account.user_type_id.type in ('receivable','payable')
                    user_type = getattr(account, 'user_type_id', False)
                    if user_type and getattr(user_type, 'type', False):
                        return user_type.type in ('receivable', 'payable')
                    # Odoo 17-18: account.account.account_type in ('asset_receivable','liability_payable')
                    acc_type = getattr(account, 'account_type', False)
                    return acc_type in ('asset_receivable', 'liability_payable')

                receivable_lines = inv.line_ids.filtered(_is_receivable_payable)
                counterpart_lines = self.env['account.move.line']
                for l in receivable_lines:
                    # 兼容新旧版本：使用 partial reconcile 的 debit_move_id / credit_move_id
                    partial_debits = getattr(l, 'matched_debit_ids', self.env['account.partial.reconcile'])
                    partial_credits = getattr(l, 'matched_credit_ids', self.env['account.partial.reconcile'])
                    counterpart_lines |= partial_debits.mapped('debit_move_id')
                    counterpart_lines |= partial_credits.mapped('credit_move_id')

                # 为避免逐条查找，先一次性将 move_id 映射到 payment 名称
                move_ids = list(set(counterpart_lines.mapped('move_id').ids))
                payments = self.env['account.payment'].sudo().search([('move_id', 'in', move_ids)]) if move_ids else self.env['account.payment']
                payment_name_by_move = {p.move_id.id: p.name for p in payments}

                for cl in counterpart_lines:
                    move = cl.move_id
                    # 优先用付款单号（如为收款/付款凭证），再退回凭证号/参考
                    name = payment_name_by_move.get(move.id) or move.name or move.ref
                    if name:
                        receipt_names.add(name)

            order.voucher_number = ', '.join([n for n in voucher_names if n]) or False
            order.receipt_number = ', '.join(sorted(receipt_names)) or False
