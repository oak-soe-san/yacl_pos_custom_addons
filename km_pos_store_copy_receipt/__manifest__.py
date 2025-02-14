# -*- coding: utf-8 -*-
{
    'name': 'KM POS Store Copy Receipt',
    'version': '16.0.0',
    'description': 'This module allow to print store copy receipt on pos.',
    'summary': 'User can print store copy receipt on pos.',
    'category': 'Hidden/Tests',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    'depends': ['base', 'point_of_sale', 'sync_pos_currency', 'bi_pos_multi_receipt'],
    "data": [
        "views/res_config_settings_views.xml"
    ],
    'assets': {
        'point_of_sale.assets': [
            'km_pos_store_copy_receipt/static/src/css/receipt.css',
            'km_pos_store_copy_receipt/static/src/js/models.js',
            'km_pos_store_copy_receipt/static/src/js/Screens/ReceiptScreen/StoreCopyReceipt.js',
            'km_pos_store_copy_receipt/static/src/xml/**/*'
        ],
    },
    'installable': True,
    'auto_install': False
}
