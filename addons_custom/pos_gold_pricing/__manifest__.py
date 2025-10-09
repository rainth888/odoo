
{
    "name": "POS Gold Pricing",
    "version": "18.0.2.0",
    "summary": "POS 动态计价（黄金/首饰：净金重×当日金价+工费）",
    "category": "Point of Sale",
    "website": "https://example.com",
    "author": "Your Team",
    "license": "LGPL-3",
    "depends": ["point_of_sale", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/metal_type_views.xml",
        "views/metal_pricelist_views.xml",
        "views/stock_production_lot_views.xml",
        "views/product_template_views.xml",
    ],
    "assets": {
        # 暂时移除对 POS 前端的注入以避免白屏，待补丁稳定后再恢复
        # "point_of_sale._assets_pos": [
        #     "pos_gold_pricing/static/src/js/pos_gold_pricing.js"
        # ]
    },
    "installable": True,
    "application": False
}
