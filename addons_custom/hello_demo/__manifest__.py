# -*- coding: utf-8 -*-
{
    "name": "Hello Demo",
    "summary": "A minimal Odoo 18 module: model + views + menu + ACL",
    "version": "1.0.0",
    "category": "Tools",
    "author": "You",
    "website": "",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/hello_item_views.xml",
        # "data/demo_data.xml",  # 如需演示数据，取消注释
    ],
    "application": True,     # 在应用面板显示“Hello Demo”卡片
    "installable": True,
}