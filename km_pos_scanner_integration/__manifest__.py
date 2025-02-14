{
    'name': 'KM POS Scanner Integration',
    'version': '16.1.0',
    'description': 'This module allow to scan passport scanner at pos.',
    'summary': 'User can scan pos passport scanner.',
    'category': 'Point of Sale',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    "depends": [
        "point_of_sale",
        "km_pos_store_copy_receipt"
    ],
    "data": [
        "views/view_res_partner.xml",
        "views/view_pos_order.xml",
        "views/res_config_settings_views.xml"
    ],
    "assets": {
        "point_of_sale.assets": [
            "km_pos_scanner_integration/static/src/css/km_pos_scanner_integration.scss",
            "km_pos_scanner_integration/static/src/xml/PartnerDetailsEdit.xml",
            "km_pos_scanner_integration/static/src/xml/StoreCopyReceipt.xml",
            "km_pos_scanner_integration/static/src/xml/OrderReceipt.xml",
            "km_pos_scanner_integration/static/src/js/**/*.js"
        ]
    },
    'installable': True,
    'auto_install': False
}
