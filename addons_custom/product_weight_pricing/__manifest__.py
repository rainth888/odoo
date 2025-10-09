{
    "name": "Product Weight & Pricing Method",
    "version": "18.0.1.5",
    "summary": "Expose Weight, UoM, and a Pricing Method for gold products",
    "category": "Product",
    "author": "Your Team",
    "license": "LGPL-3",
    "depends": ["product", "uom", "pos_gold_pricing"],
    "data": [
        "views/product_template_views.xml"
    ],
    "assets": {
        "point_of_sale.assets": [
            "addons_custom/product_weight_pricing/static/src/js/pos_pricing_method.js",
            "addons_custom/product_weight_pricing/static/src/xml/pos_weight_orderline.xml",
        ],
    },
    "installable": True,
}
