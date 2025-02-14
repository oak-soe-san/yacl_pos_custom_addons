{
    'name': 'KM POS Currency',
    'version': '16.0.0',
    'description': 'This module add final change value at sync_pos_currency',
    'category': 'Point of Sale',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    'depends': ['sync_pos_currency'],
    'assets': {
        'point_of_sale.assets': [
            'km_pos_currency/static/src/js/**/*.js',
            'km_pos_currency/static/src/xml/**/*'
        ]
    },
    'installable': True,
    'auto_install': False
}
