# -*- coding: utf-8 -*-
{
    'name': "Multi Point of Sale Management System",

    'summary': """
        POS Management System""",

    'description': """
        Multi POS Management System Module which is developed by IZEL OPEN SOURCE BUSINESS MANAGEMENT.
    """,

    'author': "IZEL - OPEN SOURCE BUSINESS MANAGEMENT",
    'website': "https://www.yourcompany.com",
    'sequence': 2,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'pos_restaurant', 'report_xlsx',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/pos_management_system_security.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
        'wizard/hourly_sale_wizard.xml',
        'wizard/shift_report_wizard.xml',
        'wizard/monthly_sale_report.xml',
        'wizard/sale_item_menu_group.xml',
        'wizard/action_wizard.xml',
        'views/action.xml',
        'views/menu.xml',
        'views/izel_point_of_sale.xml',
        'views/contact_member_ship.xml',
        'views/inventory_inherit.xml',
        'views/res_config_settings_view.xml',
        'views/pos_integration.xml',
        'report/hourly_sale_report.xml',
        'report/shift_report.xml',
        'report/monthly_sale_report.xml',
        'report/sale_item_menu_group_report.xml',
        'report/action_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'assets': {
        'point_of_sale.assets': [
            'pos_management_system/static/src/xml/OrderReceipt.xml',
        ],
    },
}
