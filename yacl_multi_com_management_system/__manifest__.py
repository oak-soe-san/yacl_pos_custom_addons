# -*- coding: utf-8 -*-
{
    'name': "YACL Multi Company POS Management System",

    'summary': """
        POS Management System""",

    'description': """
        YACL POS Management System Module which is developed by Hledan Centre Property Management
    """,

    'author': "Hledan Centre Property Management",
    'website': "https://hledancentreproperty.com/",
    'sequence': 2,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/yacl_multi_company_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/yacl_point_of_sale.xml',
        'views/yacl_inventory.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application' : True
}
