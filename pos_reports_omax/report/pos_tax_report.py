# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError
from itertools import groupby
from operator import itemgetter

class POSTaxReceiptReport(models.AbstractModel):

    _name = 'report.pos_reports_omax.pos_tax_receipt'
    _description = 'POS Tax Receipt'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        data = data if data is not None else {}
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        #Comapny
        company_id_lst = []
        if docs.company_ids:
            company_ids = docs.company_ids
            company_id_lst = company_ids.ids
        else:
            company_ids = self.env["res.company"].search([])
            company_id_lst = company_ids.ids
        #Users  
        user_ids_lst = []
        if docs.user_ids:
            user_ids = docs.user_ids
            user_ids_lst = user_ids.ids
        else:
            user_ids = self.env["res.users"].search([])
            user_ids_lst = user_ids.ids
        #POS Config
        pos_config_ids_lst = []
        if docs.pos_config_ids:
            pos_config_ids = docs.pos_config_ids
            pos_config_ids_lst = pos_config_ids.ids
        else:
            pos_config_ids = self.env["pos.config"].search([])
            pos_config_ids_lst = pos_config_ids.ids
        
            
        start_date = docs.start_date
        end_date = docs.end_date
        
        pos_orders = self.env['pos.order'].search(
            [('user_id', 'in', user_ids_lst), ('config_id', 'in', pos_config_ids_lst),
             ('company_id', 'in', company_id_lst), ('date_order', '>=', start_date), ('date_order', '<=', end_date)])

        tax_dict_list = []
        for order in pos_orders:
            for order_line in order.lines:
                taxes = order_line.tax_ids.filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
                fiscal_position_id = order_line.order_id.fiscal_position_id
                if fiscal_position_id:
                    taxes = fiscal_position_id.map_tax(taxes, order_line.product_id, order_line.order_id.partner_id)
                price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
                taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty, product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
                for tax_dict in taxes:
                    tax_dict.update({'order_ref': order.name})
                    tax_dict_list.append(tax_dict)
        
        grouper = itemgetter("name", "order_ref")
        result = []
        total_tax_amount = 0
        for key, grp in groupby(sorted(tax_dict_list, key = grouper), grouper):
            temp_dict = dict(zip(["name", "order_ref"], key))
            total_amount = 0
            total_base = 0
            for item in grp:
                total_amount += item["amount"]
                total_base += item["base"]
                total_tax_amount += item["amount"]
            temp_dict["amount"] = total_amount
            temp_dict["base"] = total_base
            result.append(temp_dict)
        
        pos_order_tax_result = sorted(result, key = lambda i: i['order_ref'],reverse=True)
        
        tax_result = []
        second_result = sorted(pos_order_tax_result,key = itemgetter('name'))
        for key, value in groupby(second_result,key = itemgetter('name')):
            tax_temp_dict = {'tax_name': key}
            total_temp_tax_amount = 0
            for k in value:
                total_temp_tax_amount += k['amount']
            tax_temp_dict.update({'tax_amount': total_temp_tax_amount})
            tax_result.append(tax_temp_dict)
        
        tax_result = sorted(tax_result, key = lambda i: i['tax_name'],reverse=True)
        
        return {
            'doc_ids': self.ids,
            'doc_model': 'model',
            'docs': docs,
            'data': data,
            'tax_dict_list' : pos_order_tax_result,
            'tax_result': tax_result,
            'total_tax_amount': total_tax_amount,
        }
