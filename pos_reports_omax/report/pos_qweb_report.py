# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError

class LeadQwebReport(models.AbstractModel):
    _name = 'report.pos_reports_omax.pos_report'
    _description = 'Point Of Sale Qweb Report'

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

        if docs.user_ids:
            user_ids = docs.user_ids
        else:
            user_ids = self.env["res.users"].search([])
        if docs.pos_config_ids:
            pos_config_ids = docs.pos_config_ids
        else:
            pos_config_ids = self.env["pos.config"].search([])
        if docs.product_ids:
            product_ids = docs.product_ids
        else:
            product_ids = self.env['product.product'].search([])
        if docs.product_categ_ids:
            product_categ_ids = docs.product_categ_ids
        else:
            product_categ_ids = self.env['product.category'].search([])

        start_date = docs.start_date
        end_date = docs.end_date
        start_date.strftime('%m-%d-%Y 00:00:00')
        end_date.strftime('%m-%d-%Y 23:59:59')
        user_ids_lst = []
        if user_ids:
            user_ids_lst = user_ids.ids

        if docs.appiled_on == 'Product Variant':
            product_ids_lst = []
            if product_ids:
                for products in product_ids:
                    product_ids_lst.append(products)

        elif docs.appiled_on == 'All Product':
            product_ids_lst = []
            if product_ids:
                for products in product_ids:
                    product_ids_lst.append(products)
        else:
            product_ids_lst = []

        company_id_lst = []
        if company_ids:
            company_id_lst = company_ids.ids

        if docs.appiled_on == 'Product Category':
            product_categ_lst = []
            if product_categ_ids:
                for product_categ in product_categ_ids:
                    product_categ_lst.append(product_categ)
        else:
            product_categ_lst = []

        pos_config_ids_lst = []
        if pos_config_ids:
            pos_config_ids_lst = pos_config_ids.ids

        pos_orders = self.env['pos.order'].search(
            [('user_id', 'in', user_ids_lst), ('config_id', 'in', pos_config_ids_lst),
             ('company_id', 'in', company_id_lst), ('date_order', '>=', start_date), ('date_order', '<=', end_date)])
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
        return {
            'doc_ids': self.ids,
            'doc_model': 'model',
            'docs': docs,
            'data': data,
            'product_ids': product_ids,
        }
