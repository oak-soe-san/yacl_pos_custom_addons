# -*- coding: utf-8 -*-
{
    'name': 'Create MRP Order From POS',
    'version': '16.0.0.1',
    'category': 'MRP/Point of Sale',
    'summary': 'Create Manufacturing order from pos screen and view the manufacturng order created fom pos',
    'description': '''
        Create Manufacturing order from pos screen and view the manufacturng order created fom pos
    ''',
    'author': 'Warlock Technologies Pvt Ltd.',
    'website': 'http://warlocktechnologies.com',
    'support': 'support@warlocktechnologies.com',
    'depends': ['point_of_sale','mrp'],
    'data': ['views/pos_config_view.xml'],
    'assets': {
        'point_of_sale.assets': [
            'wt_create_mrp_order_from_pos/static/src/js/custome.js',
        ],
    },
    "images": ['image/screen_image.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
    'external_dependencies': {
    },
}