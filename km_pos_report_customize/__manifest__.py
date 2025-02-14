{
    'name': 'KM POS Report Customize',
    'version': '16.0.0',
    'description': 'This module fix pos_reports_omax requirement.',
    'summary': 'Fix pos_reports_omax requirement.',
    'category': 'Point of Sale',
    'author': 'Kanaung Myanmar Software Co.,Ltd',
    'website': 'https://kanaungmyanmarsoftware.com',
    "depends": [
            "pos_reports_omax", 
            "km_pos_global_discount_tax_exclusive",
            "bi_pos_combo",
            "pos_loyalty"
        ],
    "data": [
        'views/report_pos_session.xml',
        'views/report_saledetails.xml'
    ],
    'installable': True,
    'auto_install': False
}