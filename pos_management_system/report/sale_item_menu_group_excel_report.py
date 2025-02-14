# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class SaleItemMenuGroupXlsx(models.AbstractModel):
    _name = "report.pos_management_system.sale_item_excel_report_template"
    _inherit = "report.report_xlsx.abstract"


    def generate_xlsx_report(self, workbook, data, orders):
        print("Hello World")
