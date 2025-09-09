# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    receipt_paper_width = fields.Selection(
        [('58', '58mm'), ('80', '80mm')],
        string='小票纸宽', related='company_id.receipt_paper_width', readonly=False)
    receipt_font_size = fields.Selection(
        [('8', '8px'), ('10', '10px'), ('12', '12px'), ('14', '14px')],
        string='小票字体大小', related='company_id.receipt_font_size', readonly=False)
    receipt_show_logo = fields.Boolean('显示公司Logo', related='company_id.receipt_show_logo', readonly=False)
    receipt_show_barcode = fields.Boolean('显示条码(订单号)', related='company_id.receipt_show_barcode', readonly=False)
    receipt_show_qr = fields.Boolean('显示二维码(订单号)', related='company_id.receipt_show_qr', readonly=False)
    receipt_footer_note = fields.Char('小票页脚备注', related='company_id.receipt_footer_note', readonly=False)

