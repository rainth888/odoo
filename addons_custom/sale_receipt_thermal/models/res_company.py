# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    receipt_paper_width = fields.Selection(
        [('58', '58mm'), ('80', '80mm')],
        string='小票纸宽', default='58')
    receipt_font_size = fields.Selection(
        [('8', '8px'), ('10', '10px'), ('12', '12px'), ('14', '14px')],
        string='小票字体大小', default='10')
    receipt_show_logo = fields.Boolean('显示公司Logo', default=True)
    receipt_show_barcode = fields.Boolean('显示条码(订单号)', default=True)
    receipt_show_qr = fields.Boolean('显示二维码(订单号)', default=False)
    receipt_footer_note = fields.Char('小票页脚备注', help='打印在小票底部的附加说明')

