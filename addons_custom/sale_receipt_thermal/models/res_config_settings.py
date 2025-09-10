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

    # 新增公司配置代理字段
    receipt_business_number = fields.Char('营业编号', related='company_id.receipt_business_number', readonly=False)
    receipt_promo_lines = fields.Text('宣传语', related='company_id.receipt_promo_lines', readonly=False)
    receipt_slogan = fields.Char('标语', related='company_id.receipt_slogan', readonly=False)
