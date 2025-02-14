# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError ,ValidationError

import base64
import xlwt

class PrintExcel(models.TransientModel):

    _name = 'pos.payment.excel.report'
    _description = 'Excel Report'

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Report File Name', readonly=True)

class PosReport(models.TransientModel):
    _name = 'pos.payment.report.wizard'
    _description = 'Point Of Sale Payment Report'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    company_ids = fields.Many2many('res.company', string="Company")
    pos_config_ids = fields.Many2many('pos.config', string="Point Of Sale")
    payment_methods = fields.Many2many('pos.payment.method')
    cashier_users = fields.Many2many('res.users',string="Cashier User")

    def pos_payment_report_pdf(self):
        if self.end_date < self.start_date:
            raise ValidationError('Sorry, End Date Must be greater Than Start Date...')
        self.ensure_one()
        data = {}
        data['form'] = self.read(['start_date', 'end_date', 'company_ids'])[0]
        return self.env.ref('pos_reports_omax.action_pos_payment_report').report_action(self, data=data)

    def pos_payment_report_excel(self):
        if self.end_date < self.start_date:
            raise ValidationError('Sorry, End Date Must be greater Than Start Date...')
        workbook = xlwt.Workbook()
        style = xlwt.XFStyle()
        style_center = xlwt.easyxf(
            'align:vertical center, horizontal center; font:bold on; pattern: pattern solid, fore_colour gray25; border: top thin, bottom thin, right thin, left thin;')
        style_center2 = xlwt.easyxf(
            'align:vertical center, horizontal center;'
        )
        main_title = xlwt.easyxf(
            'align:vertical center, horizontal center; font:bold on; font:height 300; borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')
        table_title = xlwt.easyxf(
            'align:vertical center, horizontal center; font:bold on; font:height 220; borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.height = 250
        style.font = font

        worksheet = workbook.add_sheet('Sheet 1')
        worksheet.write_merge(0, 1, 0, 4, 'POS Payment Report', main_title)
        row = 3
        col = 0
        start_date = self.start_date
        final_start_date = start_date.strftime("%d/%m/%Y")
        worksheet.write(row, col, 'Start Date :')
        worksheet.write(row, 1, str(final_start_date))
        end_date = self.end_date
        final_end_date = end_date.strftime("%d/%m/%Y")
        worksheet.write(row, 3, 'End Date :')
        worksheet.write(row, 4, str(final_end_date))
        row += 1
        col = 0

        if self.company_ids:
            company_ids = self.company_ids
        else:
            company_ids = self.env["res.company"].search([])
        if self.cashier_users:
            cashier_users = self.cashier_users
        else:
            cashier_users = self.env["res.users"].search([])
        if self.pos_config_ids:
            pos_config_ids = self.pos_config_ids
        else:
            pos_config_ids = self.env["pos.config"].search([])
        if self.payment_methods:
            payment_methods = self.payment_methods
        else:
            payment_methods = self.env['pos.payment.method'].search([])
        start_date = self.start_date
        end_date = self.end_date
        start_date.strftime('%m-%d-%Y 00:00:00')
        end_date.strftime('%m-%d-%Y 23:59:59')
        if company_ids:
            company_id_lst = []
            company_id_lst = company_ids.ids
        if pos_config_ids:
            pos_config_ids_lst = []
            pos_config_ids_lst = pos_config_ids.ids
        if payment_methods:
            payment_methods_lst = []
            payment_methods_lst = payment_methods.ids

        for users in cashier_users:
            pos_orders = self.env['pos.order'].search([('user_id', '=', users.id), ('company_id', 'in', company_id_lst),('config_id', 'in', pos_config_ids_lst), ('date_order', '>=', start_date),('date_order', '<=', end_date),('payment_ids.payment_method_id','in',payment_methods_lst)])
            if pos_orders:
                worksheet.write_merge(row,row,col,col + 4,'User :- '+ str(users.name), table_title)
                row += 1
            for payment_method in payment_methods:
                pos_order = self.env['pos.order'].search([('user_id', '=', users.id), ('company_id', 'in', company_id_lst),('config_id', 'in', pos_config_ids_lst),('date_order', '>=', start_date),('date_order', '<=', end_date),('payment_ids.payment_method_id','=',payment_method.id)])
                if pos_order:
                    worksheet.write_merge(row,row,col,col+4,'Payment Method :- '+ str(payment_method.name),table_title)
                    row += 1
                    worksheet.write_merge(row, row + 1, col, col, 'Date', style_center)
                    worksheet.col(col).width = 256 * 20
                    col += 1
                    worksheet.write_merge(row, row + 1, col, col, 'Order', style_center)
                    worksheet.col(col).width = 256 * 18
                    col += 1
                    worksheet.write_merge(row, row + 1, col, col, 'Session', style_center)
                    worksheet.col(col).width = 256 * 18
                    col += 1
                    worksheet.write_merge(row, row + 1, col, col, 'Customer', style_center)
                    worksheet.col(col).width = 256 * 20
                    col += 1
                    worksheet.write_merge(row, row + 1, col, col, 'Amount', style_center)
                    worksheet.col(col).width = 256 * 18
                    row += 2
                    col = 0
                    total_amt = 0.0
                    for pos_orders in pos_order:
                        sub_total = 0.0
                        final_order_date = pos_orders.date_order.strftime("%d/%m/%Y")
                        worksheet.write(row,col,str(final_order_date),style_center2)
                        col += 1
                        if pos_orders.name:
                            worksheet.write(row,col,str(pos_orders.name),style_center2)
                            col += 1
                        else:
                            worksheet.write(row, col, '', style_center2)
                            col += 1
                        worksheet.write(row,col,str(pos_orders.session_id.name),style_center2)
                        col += 1
                        if pos_orders.partner_id.name:
                            worksheet.write(row,col,str(pos_orders.partner_id.name),style_center2)
                            col += 1
                        else:
                            worksheet.write(row, col, '', style_center2)
                            col += 1
                        amount_paid = "{:,.2f}".format(pos_orders.amount_paid, 0.00)
                        worksheet.write(row,col,str(amount_paid),style_center2)
                        sub_total += pos_orders.amount_paid
                        total_amt += sub_total
                        row += 1
                        col = 0
                    worksheet.write(row, 3,'Total',table_title)
                    col += 1
                    total_amt = "{:,.2f}".format(total_amt, 0.00)
                    worksheet.write(row,4,total_amt,table_title)
                    row += 1
                    col = 0

        filename = 'Point Of Sale Payment Excel.xls'
        workbook.save('/tmp/'+filename)
        file = open('/tmp/'+filename, "rb")
        file_data = file.read()
        #out = base64.encodestring(file_data)
        out = base64.encodebytes(file_data)#python3.8 support
        export_id = self.env['pos.payment.excel.report'].sudo().create({'excel_file': out, 'file_name': filename})

        return {
            'view_mode': 'form', 'res_id': export_id.id, 'res_model': 'pos.payment.excel.report', 'view_type': 'form',
            'type': 'ir.actions.act_window', 'context': self._context, 'target': 'new',
        }
