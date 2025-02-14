# -*- coding: utf-8 -*-
{
    'name': 'POS Receipt Tax Configuration',
    'summary': """POS receipt tax configuration.""",
    'description': """POS receipt tax configuration.""",
    'sequence': '1',
    'category': 'Point of Sale',
    'author': "Creyox Technologies",
    'depends': ['point_of_sale'],
    'version': '16.0.0.1',
    'price': '25.0',
    'currency': 'USD',
    'license': 'AGPL-3',
    'data': [
        'views/res_config_settings_view.xml'
    ],
    'images': ['static/description/banner.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_tax_conf/static/src/xml/OrderReceipt.xml',
        ],
    },
}
