{
    'name': 'Secondary Currency Rounding',
    'version': '16.0.0',
    'description': 'This module rounding Up and Down 50 secondary currency at pro forma slip',
    'category': 'Point of Sale',
    'author': 'Mingalarsky Co.,Ltd',
    'website': 'https://www.mingalarsky.com',
    'depends': ['base','point_of_sale','km_pos_currency'],
    'assets': {
        'point_of_sale.assets': [
            'mscl_pos_sec_currency_round/static/src/xml/MultiCurrencyOrderReceipt.xml',
            'mscl_pos_sec_currency_round/static/src/js/Popups/RoundMultiCurrencyPopup.js',
            
        ]
    },
    'installable': True,
    'auto_install': False
}
