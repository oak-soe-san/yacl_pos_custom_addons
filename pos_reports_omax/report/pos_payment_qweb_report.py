# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError

class LeadQwebReport(models.AbstractModel):
    _name = 'report.pos_reports_omax.pos_payment_report'
    _description = 'Point Of Sale Payment Qweb Report'

    def _get_cashier_user(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        if docs.cashier_users:
            cashier_users = docs.cashier_users
        else:
            cashier_users = self.env["res.users"].search([])
        return cashier_users

    def _get_payment_method(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        if docs.payment_methods:
            payment_methods = docs.payment_methods
        else:
            payment_methods = self.env['pos.payment.method'].search([])
        return payment_methods

    def _get_pos_orders(self,user, payment_method,company_id_lst,pos_config_ids_lst,start_date,end_date):
        pos_order = self.env['pos.order'].search([('user_id', '=', user.id), ('company_id', 'in', company_id_lst),('config_id', 'in', pos_config_ids_lst), ('date_order', '>=', start_date),('date_order', '<=', end_date), ('payment_ids.payment_method_id', '=', payment_method.id)])
        return pos_order

    def _get_pos_orders_found(self,user, payment_method,company_id_lst,pos_config_ids_lst,start_date,end_date):
        if payment_method:
            payment_methods_lst = []
            payment_methods_lst = payment_method.ids
        pos_orders = self.env['pos.order'].search([('user_id', '=', user.id), ('company_id', 'in', company_id_lst),('config_id', 'in', pos_config_ids_lst), ('date_order', '>=', start_date),('date_order', '<=', end_date), ('payment_ids.payment_method_id', 'in', payment_methods_lst)])
        return pos_orders

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        data = data if data is not None else {}
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        if docs.company_ids:
            company_ids = docs.company_ids
        else:
            company_ids = self.env["res.company"].search([])
        if docs.pos_config_ids:
            pos_config_ids = docs.pos_config_ids
        else:
            pos_config_ids = self.env["pos.config"].search([])
        start_date = docs.start_date
        end_date = docs.end_date
        start_date.strftime('%m-%d-%Y 00:00:00')
        end_date.strftime('%m-%d-%Y 23:59:59')

        if company_ids:
            company_id_lst = []
            company_id_lst = company_ids.ids
        if pos_config_ids:
            pos_config_ids_lst = []
            pos_config_ids_lst = pos_config_ids.ids

        return {
            'doc_ids': self.ids,
            'doc_model': 'model',
            'docs': docs,
            'data': data,
            'company_id_lst' : company_id_lst,
            'pos_config_ids_lst': pos_config_ids_lst,
            'start_date': start_date,
            'end_date': end_date,
            'get_cashier_user' : self._get_cashier_user,
            'get_payment_method':self._get_payment_method,
            'get_pos_orders':self._get_pos_orders,
            'get_pos_orders_found' : self._get_pos_orders_found,
        }
