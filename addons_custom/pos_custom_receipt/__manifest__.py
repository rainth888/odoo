# -*- coding: utf-8 -*-
{
    'name': 'POS Custom Receipt (Thermal Style)',
    'summary': '自定义 POS 小票样式，复用热敏票据风格',
    'version': '1.1.0',
    'category': 'Point of Sale',
    'author': 'Your Company',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'sale_receipt_thermal'],
    'data': [],
    'assets': {
        # 注入到 PoS 前端资源包（Odoo 18 使用 _assets_pos / assets_prod 体系）
        'point_of_sale._assets_pos': [
            'pos_custom_receipt/static/src/xml/pos_custom_receipt.xml',
            'pos_custom_receipt/static/src/css/receipt.css',
        ],
    },
    'installable': True,
    'application': True,
}
