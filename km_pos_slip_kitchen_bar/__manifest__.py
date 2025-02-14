{
    'name': 'KM POS Slip Kitchen Bar',
    'version': '16.0.0',
    'description': 'This module allow you to export POS slip to kitchen and bar.',
    'summary': 'User can print POS slip to kitchen and bar.',
    'category': 'Point of Sale',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    'depends': ['base', 'point_of_sale', 'pos_restaurant'],
    'data': [
            'views/kitchen_bar_slip_views.xml',
            'views/res_config_settings_views.xml',
            'security/ir.model.access.csv',
            'security/point_of_sale_security.xml'
        ],
    'assets': {
        'point_of_sale.assets': [
            'km_pos_slip_kitchen_bar/static/src/js/**/*.js',
            'km_pos_slip_kitchen_bar/static/src/xml/**/*'
        ]
    },
    'installable': True,
    'auto_install': False
}
