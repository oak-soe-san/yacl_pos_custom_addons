{
    'name': 'POS IP Address Print',
    'version': '16.0.0.0',
    'category': 'Website',
    'license': 'AGPL-3',
    'description': """
Point of Sales print with ip address
====================================
Network printer will print receipt.
    """,
    'author': 'Mingalar Sky Co., Ltd.',
    'website': 'https://www.mingalarsky.com',
    'depends': ['base', 'web', 'point_of_sale'],
    'data': [
            'security/ir.model.access.csv',
            'security/security.xml',
            'views/printers_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mscl_pos_ip_print/static/src/js/*.js',
        ],
    },
    'installable': True,
    'active': False,
}