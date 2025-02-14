# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Currency Exchange ProForma',
    'category': 'Sales/Point of Sale',
    'summary': 'This module is used to customized receipt of point of sale when a user adds a product in the cart and validates payment and print receipt, then the user can see the client name on POS Receipt. | Custom Receipt | POS Reciept | Payment | POS Custom Receipt',
    'description': "Customized our point of sale receipt",
    'version': '16.0.1.0',
    'website': 'https://www.mingalarsky.com',
    'author': 'Mingalar Sky Co.,Ltd',
    # 'images': ['static/description/icon.png'],
    'depends': ['base', 'point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'proforma_currency/static/src/xml/proforma_currency.xml'

        ],
    },
    'installable': True,
}
