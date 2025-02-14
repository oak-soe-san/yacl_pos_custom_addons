{
    'name': 'Customer ID',
    'version': '16.0.0',
    'description': 'This module add button Custom Customer ID',
    'category': 'Point of Sale',
    'author': 'Mingalar Sky Co., Ltd.',
    'website': 'https://www.mingalarsky.com',
    'depends': ['point_of_sale','web','base'],
    'assets': {
        'point_of_sale.assets': [
            'mscl_pos_customer_id/static/src/js/**/*.js',
            'mscl_pos_customer_id/static/src/xml/**/*'
        ]
    },
    'installable': True,
    'auto_install': False
}
