##############################################################################
#    LIXIE STUDIO (<https://lixie.io>)
#    Copyright (C) 2020-ACTUAL Lixie Studio Digital, C.A.
#    Contact: hola@lixie.io | +58(412)549.43.83
##############################################################################
{
    'name': 'Internal Reference in POS',
    'summary': "Displays the internal product code in each POS items",
    'description': """
        A simple module that adds the internal reference number above 
        the name of the products in each POS item.
    """,
    'author': 'Lixie Studio',
    'website': 'https://lixie.io',
    'category': 'Uncategorized',
    'version': '16.0.1',
    'depends': ['base', 'point_of_sale'],
    'data': [
        # 'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'internal_reference_in_pos/static/src/scss/**/*',
            # 'internal_reference_in_pos/static/src/js/**/*',
            'internal_reference_in_pos/static/src/xml/**/*',
        ],
    },
    'license': 'LGPL-3',
    'images': ['static/description/Banner.png'],
}