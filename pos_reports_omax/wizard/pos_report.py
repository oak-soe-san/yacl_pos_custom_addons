# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import Counter

from odoo import api, fields, models ,SUPERUSER_ID
import time
from datetime import datetime
import calendar

import base64
import xlwt
from odoo.exceptions import UserError ,ValidationError

class PrintExcel(models.TransientModel):

    _name = 'pos.excel.report'
    _description = 'Excel Report'

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Report File Name', readonly=True)

class PosReport(models.TransientModel):
    _name = 'pos.report.wizard'
    _description = 'Point Of Sale Report'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    company_ids = fields.Many2many('res.company', string="Company")
    appiled_on = fields.Selection([('All Product', 'All Product'),('Product Variant', 'Product Variant'), ('Product Category', 'Product Category')],
                                 string='Appiled On', default='All Product')
    product_ids = fields.Many2many('product.product', string="Product")
    product_categ_ids = fields.Many2many('product.category', string="Product Category")
    user_ids = fields.Many2many('res.users', string="Users")
    pos_config_ids = fields.Many2many('pos.config', string="Point Of Sale")

    def pos_report_pdf(self):
        if self.end_date < self.start_date:
            raise ValidationError('Sorry, End Date Must be greater than or equal to Start Date...')
        self.ensure_one()
        data = {}
        data['form'] = self.read(['start_date', 'end_date','company_ids'])[0]
        return self.env.ref('pos_reports_omax.action_pos_report').report_action(self, data=data)

    @api.onchange("appiled_on")
    def _onchage_appiled_on(self):
        if self.appiled_on == 'All Product':
            self.product_ids = [(6, 0, [])]
            self.product_categ_ids = [(6, 0,[])]
        elif self.appiled_on == 'Product Variant':
            self.product_categ_ids = [(6, 0, [])]
        else:
            self.product_ids = [(6, 0, [])]

    def pos_report_excel(self):
        if self.end_date < self.start_date:
            raise ValidationError('Sorry, End Date Must be greater than or equal to Start Date...')

        workbook = xlwt.Workbook()
        style = xlwt.XFStyle()
        style_center = xlwt.easyxf(
            'align:vertical center, horizontal center; font:bold on; pattern: pattern solid, fore_colour gray25; border: top thin, bottom thin, right thin, left thin;')
        style_center2 = xlwt.easyxf(
            'align:vertical center, horizontal center;'
        )
        main_title = xlwt.easyxf('align:vertical center, horizontal center; font:bold on; font:height 300; borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.height = 250
        style.font = font

        worksheet = workbook.add_sheet('Sheet 1')
        worksheet.write_merge(0, 1, 0, 11,'Weekdays POS Report',main_title)
        row = 3
        col = 0
        start_date = self.start_date
        final_start_date = start_date.strftime("%d/%m/%Y")
        worksheet.write(row, col ,'Start Date :')
        worksheet.write(row,1,str(final_start_date))
        end_date = self.end_date
        final_end_date = end_date.strftime("%d/%m/%Y")
        worksheet.write(row,5,'End Date :')
        worksheet.write(row,6,str(final_end_date))

        if self.company_ids:
            company_ids = self.company_ids
        else:
            company_ids = self.env["res.company"].search([])
        if self.user_ids:
            user_ids = self.user_ids
        else:
            user_ids = self.env["res.users"].search([])
        if self.pos_config_ids:
            pos_config_ids = self.pos_config_ids
        else:
            pos_config_ids = self.env["pos.config"].search([])
        if self.product_ids:
            product_ids = self.product_ids
        else:
            product_ids = self.env['product.product'].search([])
        if self.product_categ_ids:
            product_categ_ids = self.product_categ_ids
        else:
            product_categ_ids = self.env['product.category'].search([])

        start_date = self.start_date
        end_date = self.end_date
        start_date.strftime('%m-%d-%Y 00:00:00')
        end_date.strftime('%m-%d-%Y 23:59:59')

        row += 2
        col = 0

        worksheet.write_merge(row, row + 1, col,col + 2,'Product Name',style_center)
        worksheet.col(col).width = 256 * 22
        col += 3
        worksheet.write_merge(row, row + 1, col,col,'Monday', style_center)
        col += 1
        worksheet.write_merge(row, row + 1, col,col, 'Tuesday', style_center)
        col += 1
        worksheet.write_merge(row, row + 1, col,col, 'Wednesday', style_center)
        col += 1
        worksheet.write_merge(row, row + 1, col,col, 'Thursday', style_center)
        col += 1
        worksheet.write_merge(row, row + 1, col,col, 'Friday', style_center)
        col += 1
        worksheet.write_merge(row, row + 1, col,col, 'Saturday', style_center)
        col += 1
        worksheet.write_merge(row, row + 1, col, col, 'Sunday', style_center)
        col += 1
        worksheet.write_merge(row, row + 1, col,col + 1, 'Total', style_center)

        col = 0
        row += 2

        user_ids_lst = []
        if user_ids:
            user_ids_lst = user_ids.ids

        if self.appiled_on == 'All Product':
            product_ids_lst = []
            if product_ids:
                for products in product_ids:
                    product_ids_lst.append(products)

        elif self.appiled_on == 'Product Variant':
            product_ids_lst = []
            if product_ids:
                for products in product_ids:
                    product_ids_lst.append(products)
        else:
            product_ids_lst = []

        company_id_lst = []
        if company_ids:
            company_id_lst = company_ids.ids

        if self.appiled_on == 'Product Category':
            product_categ_lst = []
            if product_categ_ids:
                for product_categ in product_categ_ids:
                    product_categ_lst.append(product_categ)
        else:
            product_categ_lst = []

        pos_config_ids_lst = []
        if pos_config_ids:
            pos_config_ids_lst = pos_config_ids.ids

        pos_orders = self.env['pos.order'].search([('user_id', 'in' , user_ids_lst),('config_id', 'in' , pos_config_ids_lst),('company_id', 'in' ,company_id_lst),('date_order','>=',start_date),('date_order','<=',end_date)])
        if pos_orders:
            if product_ids_lst:
                pos_order_lines = pos_orders.mapped('lines')
                product_ids = {}
                dayname = {0: 'mon',1:'tue',2:'wed',3:'thurs',4:'fri',5:'sat',6:'sun'}
                for order_line in pos_order_lines:
                    if order_line.product_id in product_ids_lst:
                        day = {}
                        mon_total = 0
                        tue_total = 0
                        wed_total = 0
                        thurs_total = 0
                        fri_total = 0
                        sat_total = 0
                        sun_total = 0
                        product_id = order_line.product_id
                        if product_id not in product_ids:
                            weekday = order_line.create_date.weekday()
                            if weekday == 0:
                                mon_total += order_line.qty
                                day['mon'] = mon_total
                            if weekday == 1:
                                tue_total += order_line.qty
                                day['tue'] = tue_total
                            if weekday == 2:
                                wed_total += order_line.qty
                                day['wed'] = wed_total
                            if weekday == 3:
                                thurs_total += order_line.qty
                                day['thurs'] = thurs_total
                            if weekday == 4:
                                fri_total += order_line.qty
                                day['fri'] = fri_total
                            if weekday == 5:
                                sat_total += order_line.qty
                                day['sat'] = sat_total
                            if weekday == 6:
                                sun_total += order_line.qty
                                day['sun'] = sun_total
                            product_ids[product_id] = day
                        else:
                            weekday = order_line.create_date.weekday()
                            if weekday == 0:
                                if dayname[weekday] in product_ids[product_id]:
                                    monday_value = product_ids[product_id]
                                    product_ids[product_id]['mon'] = order_line.qty + monday_value['mon']
                                else:
                                    product_ids[product_id].update({'mon': order_line.qty})
                            if weekday == 1:
                                if dayname[weekday] in product_ids[product_id]:
                                    tuesday_value = product_ids[product_id]
                                    product_ids[product_id]['tue'] = order_line.qty + tuesday_value['tue']
                                else:
                                    product_ids[product_id].update({'tue': order_line.qty})
                            if weekday == 2:
                                if dayname[weekday] in product_ids[product_id]:
                                    wednesday_value = product_ids[product_id]
                                    product_ids[product_id]['wed'] = order_line.qty + wednesday_value['wed']
                                else:
                                    product_ids[product_id].update({'wed': order_line.qty})
                            if weekday == 3:
                                if dayname[weekday] in product_ids[product_id]:
                                    thursday_value = product_ids[product_id]
                                    product_ids[product_id]['thurs'] = order_line.qty + thursday_value['thurs']
                                else:
                                    product_ids[product_id].update({'thurs': order_line.qty})
                            if weekday == 4:
                                if dayname[weekday] in product_ids[product_id]:
                                    friday_value = product_ids[product_id]
                                    product_ids[product_id]['fri'] = order_line.qty + friday_value['fri']
                                else:
                                    product_ids[product_id].update({'fri': order_line.qty})
                            if weekday == 5:
                                if dayname[weekday] in product_ids[product_id]:
                                    saturday_value = product_ids[product_id]
                                    product_ids[product_id]['sat'] = order_line.qty + saturday_value['sat']
                                else:
                                    product_ids[product_id].update({'sat': order_line.qty})
                            if weekday == 6:
                                if dayname[weekday] in product_ids[product_id]:
                                    sunday_value = product_ids[product_id]
                                    product_ids[product_id]['sun'] = order_line.qty + sunday_value['sun']
                                else:
                                    product_ids[product_id].update({'sun': order_line.qty})
            if product_categ_lst:
                pos_order_lines = pos_orders.mapped('lines')
                product_ids = {}
                dayname = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thurs', 4: 'fri', 5: 'sat', 6: 'sun'}
                for order_line in pos_order_lines:
                    if order_line.product_id.categ_id in product_categ_lst:
                        day = {}
                        mon_total = 0
                        tue_total = 0
                        wed_total = 0
                        thurs_total = 0
                        fri_total = 0
                        sat_total = 0
                        sun_total = 0
                        product_id = order_line.product_id
                        if product_id not in product_ids:
                            weekday = order_line.create_date.weekday()
                            if weekday == 0:
                                mon_total += order_line.qty
                                day['mon'] = mon_total
                            if weekday == 1:
                                tue_total += order_line.qty
                                day['tue'] = tue_total
                            if weekday == 2:
                                wed_total += order_line.qty
                                day['wed'] = wed_total
                            if weekday == 3:
                                thurs_total += order_line.qty
                                day['thurs'] = thurs_total
                            if weekday == 4:
                                fri_total += order_line.qty
                                day['fri'] = fri_total
                            if weekday == 5:
                                sat_total += order_line.qty
                                day['sat'] = sat_total
                            if weekday == 6:
                                sun_total += order_line.qty
                                day['sun'] = sun_total
                            product_ids[product_id] = day
                        else:
                            weekday = order_line.create_date.weekday()
                            if weekday == 0:
                                if dayname[weekday] in product_ids[product_id]:
                                    monday_value = product_ids[product_id]
                                    product_ids[product_id]['mon'] = order_line.qty + monday_value['mon']
                                else:
                                    product_ids[product_id].update({'mon': order_line.qty})
                            if weekday == 1:
                                if dayname[weekday] in product_ids[product_id]:
                                    tuesday_value = product_ids[product_id]
                                    product_ids[product_id]['tue'] = order_line.qty + tuesday_value['tue']
                                else:
                                    product_ids[product_id].update({'tue': order_line.qty})
                            if weekday == 2:
                                if dayname[weekday] in product_ids[product_id]:
                                    wednesday_value = product_ids[product_id]
                                    product_ids[product_id]['wed'] = order_line.qty + wednesday_value['wed']
                                else:
                                    product_ids[product_id].update({'wed': order_line.qty})
                            if weekday == 3:
                                if dayname[weekday] in product_ids[product_id]:
                                    thursday_value = product_ids[product_id]
                                    product_ids[product_id]['thurs'] = order_line.qty + thursday_value['thurs']
                                else:
                                    product_ids[product_id].update({'thurs': order_line.qty})
                            if weekday == 4:
                                if dayname[weekday] in product_ids[product_id]:
                                    friday_value = product_ids[product_id]
                                    product_ids[product_id]['fri'] = order_line.qty + friday_value['fri']
                                else:
                                    product_ids[product_id].update({'fri': order_line.qty})
                            if weekday == 5:
                                if dayname[weekday] in product_ids[product_id]:
                                    saturday_value = product_ids[product_id]
                                    product_ids[product_id]['sat'] = order_line.qty + saturday_value['sat']
                                else:
                                    product_ids[product_id].update({'sat': order_line.qty})
                            if weekday == 6:
                                if dayname[weekday] in product_ids[product_id]:
                                    sunday_value = product_ids[product_id]
                                    product_ids[product_id]['sun'] = order_line.qty + sunday_value['sun']
                                else:
                                    product_ids[product_id].update({'sun': order_line.qty})
            mon_total = 0
            tue_total = 0
            wed_total = 0
            thurs_total = 0
            fri_total = 0
            sat_total = 0
            sun_total = 0
            main_total = 0
            for key, value in product_ids.items():
                if key.product_template_attribute_value_ids:
                    key_name = ""
                    for key_names in key.product_template_attribute_value_ids:
                        key_name = key_names.name + " " + key_name
                    worksheet.write_merge(row, row, col, col + 2, str(key.name) + " " + str(key_name))
                else:
                    worksheet.write_merge(row, row, col, col + 2, str(key.name))
                total_qty = 0
                for key2, value2 in value.items():
                    if key2 == 'mon':
                        col = 3
                        worksheet.write_merge(row, row, col, col, str(value2), style_center2)
                        total_qty += value2
                        mon_total += value2
                    if key2 == 'tue':
                        col = 4
                        worksheet.write_merge(row, row, col, col, str(value2), style_center2)
                        total_qty += value2
                        tue_total += value2
                    if key2 == 'wed':
                        col = 5
                        worksheet.write_merge(row, row, col, col, str(value2), style_center2)
                        total_qty += value2
                        wed_total += value2
                    if key2 == 'thurs':
                        col = 6
                        worksheet.write_merge(row, row, col, col, str(value2), style_center2)
                        total_qty += value2
                        thurs_total += value2
                    if key2 == 'fri':
                        col = 7
                        worksheet.write_merge(row, row, col, col, str(value2), style_center2)
                        total_qty += value2
                        fri_total += value2
                    if key2 == 'sat':
                        col = 8
                        worksheet.write_merge(row, row, col, col, str(value2), style_center2)
                        total_qty += value2
                        sat_total += value2
                    if key2 == 'sun':
                        col = 9
                        worksheet.write_merge(row, row, col, col, str(value2), style_center2)
                        total_qty += value2
                        sun_total += value2
                col = 10
                worksheet.write_merge(row, row, col, col + 1, str(total_qty), style_center2)
                main_total += total_qty
                row += 1
                col = 0

            col = 0
            worksheet.write_merge(row, row, col, col + 2, 'Total', style_center)
            col += 3
            worksheet.write_merge(row, row, col, col, str(mon_total), style_center)
            col += 1
            worksheet.write_merge(row, row, col, col, str(tue_total), style_center)
            col += 1
            worksheet.write_merge(row, row, col, col, str(wed_total), style_center)
            col += 1
            worksheet.write_merge(row, row, col, col, str(thurs_total), style_center)
            col += 1
            worksheet.write_merge(row, row, col, col, str(fri_total), style_center)
            col += 1
            worksheet.write_merge(row, row, col, col, str(sat_total), style_center)
            col += 1
            worksheet.write_merge(row, row, col, col, str(sun_total), style_center)
            col += 1
            worksheet.write_merge(row, row, col, col + 1, str(main_total), style_center)
            col += 2

        filename = 'Point Of Sale Excel.xls'
        workbook.save('/tmp/'+filename)
        file = open('/tmp/'+filename, "rb")
        file_data = file.read()
        #out = base64.encodestring(file_data)
        out = base64.encodebytes(file_data)#python3.8 support
        export_id = self.env['pos.excel.report'].sudo().create({'excel_file': out, 'file_name': filename})

        return {
            'view_mode': 'form', 'res_id': export_id.id, 'res_model': 'pos.excel.report', 'view_type': 'form',
            'type': 'ir.actions.act_window', 'context': self._context, 'target': 'new',
        }
