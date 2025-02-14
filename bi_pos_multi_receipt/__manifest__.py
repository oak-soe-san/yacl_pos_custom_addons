# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "POS Multi Receipt Print",
    'version': '16.0.0.1',
    'category': 'Point of Sale',
    'summary': "Allow to print multi receipt on pos multiple receipt print point of sales multi receipt print on point of sales multiple receipt print on point of sale multi receipt print n number of receipt on pos print multi receipt on point of sales multi receipt print",
    'description': """ 

        This Odoo App helps users to print N number of receipt in point of sale. User can enable print multi receipt checkbox and set any of the number to print receipt N number of times in point of sale receipt screen.

    """,
    'author': 'BrowseInfo',
    "price": 15,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.in',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/pos_config.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'bi_pos_multi_receipt/static/src/css/receipt.css',
            'bi_pos_multi_receipt/static/src/js/Screens/ReceiptScreen/CustomAbstractReceiptScreen.js',
            'bi_pos_multi_receipt/static/src/js/Screens/ReceiptScreen/ReceiptScreen.js',
            'bi_pos_multi_receipt/static/src/xml/**/*',
        ],
    },
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/f-XrSB91UmM',
    "images":['static/description/Banner.gif'],
}

