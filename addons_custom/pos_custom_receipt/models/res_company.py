# -*- coding: utf-8 -*-
from odoo import models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        # 将 sale_receipt_thermal 定义的公司配置字段同步到 POS 前端
        extra = [
            'receipt_paper_width',
            'receipt_font_size',
            'receipt_show_logo',
            'receipt_show_barcode',
            'receipt_show_qr',
            'receipt_footer_note',
            'receipt_business_number',
            'receipt_promo_lines',
            'receipt_slogan',
        ]
        # 仅添加实际存在的字段，避免未安装依赖时报错
        model_fields = self.env['res.company'].fields_get().keys()
        fields += [f for f in extra if f in model_fields and f not in fields]
        return fields

