{
    'name': 'KM POS Combo Customize',
    'version': '16.0.0',
    'description': 'This module fix bi_pos_combo requirement.',
    'summary': 'Fix bi_pos_combo requirement.',
    'category': 'Point of Sale',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    "depends": ["bi_pos_combo"],
    "data": [
        'views/custom_pos_view.xml'
    ],
    "assets": {
        "point_of_sale.assets": [
            'km_pos_combo_customize/static/src/xml/**/*',
            "km_pos_combo_customize/static/src/js/**/*.js"
        ]
    },
    'installable': True,
    'auto_install': False
}