{
    "name": "Sale Receipt Thermal",
    "version": "18.0.1.0.11",
    "summary": "Thermal (58/80mm) PDF receipt for Sale Order",
    "category": "Sales",
    "depends": ["web", "sale_management", "account", "point_of_sale"],
    "data": [
        "views/report_sale.xml",
        "views/sale_order_view.xml",
        "views/report_account.xml",
        "views/account_move_view.xml",
        "views/report_pos.xml",
        "views/res_config_settings_view.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
