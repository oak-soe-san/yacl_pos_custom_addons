{
    'name': 'KM POS Direct Print',
    'version': '16.0.0',
    'description': 'This module allow you to direct print POS slip to kitchen and bar.',
    'summary': 'User can direct print POS slip to kitchen and bar.',
    'category': 'Point of Sale',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    'depends': ['km_pos_slip_kitchen_bar', 'direct_print_odoo'],
    'data': [
            'views/res_config_settings_views.xml',
            'views/kitchen_bar_slip_views.xml'
        ],
    'assets': {
        'point_of_sale.assets': [
            'km_pos_direct_print/static/src/js/**/*.js',
            'km_pos_direct_print/static/src/xml/**/*'
        ]
    },
    'installable': True,
    'auto_install': False
}
