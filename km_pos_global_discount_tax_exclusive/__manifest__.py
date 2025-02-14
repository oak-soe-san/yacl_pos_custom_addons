{
    'name': 'KM POS Global Discount Tax Exclusive',
    'version': '16.0.0',
    'description': 'This module fix Tax-Excluded Global Discount.',
    'summary': 'Fix Tax-Excluded Global Discount.',
    'category': 'Point of Sale',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    "depends": ["point_of_sale", "pos_loyalty"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/product_view.xml"
    ],
    "assets": {
        "point_of_sale.assets": [
            "km_pos_global_discount_tax_exclusive/static/src/js/**/*.js"
        ]
    },
    'installable': True,
    'auto_install': False
}