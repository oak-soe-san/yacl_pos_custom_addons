from odoo import _, api, fields, models
from datetime import datetime
from dateutil import tz
import pytz
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from collections import Counter
import json, ast
from itertools import groupby
from operator import itemgetter
from collections import defaultdict


class ShiftReportWizard(models.TransientModel):
    _name = 'shift.report.wizard'
    _description = 'Shift Report Wizard'

    user_id = fields.Many2one('res.users', string="User", widget='many2one', placeholder="Shops that are using User Information", domain=lambda self: [('company_ids', 'in', self.env.user.company_ids.ids)], required=True)
    session_id = fields.Many2one('pos.session', string="Session")
    date_from = fields.Datetime(string='Start From', required=True)
    date_to = fields.Datetime(string='End To', required=True)
    
    def action_print_report(self):
        start_date = self.date_from
        end_date = self.date_to
        user_id = self.user_id
        
        _domain = [('date_order', '>=', start_date),('date_order', '<=', end_date),('user_id', '=', user_id.id)]
        
        if self.session_id:
            _domain.append(('session_id', '=', self.session_id.id))
        
        pos_order_ids = self.env['pos.order'].search(_domain)

        data = {}
        data['pos_orders'] = self._get_pos_orders(pos_order_ids)
        data['user_id'] = user_id.name


        return self.env.ref('pos_management_system.shift_report_action').report_action(self,data=data)
    
    def _get_pos_orders(self,pos_order_ids):

        data_list = []
        session_ids = []
        total_net_amount = 0.0
        total_gross_amount = 0.0
        current_date_time = self.get_formated_datetime(datetime.now())
        mapped_session_ids = pos_order_ids.mapped('session_id')
        total_guest_count = self.get_guest_count_data(pos_order_ids)
        total_order_count = self.get_order_count_data(pos_order_ids)
        payment_data = self.get_payment_data(pos_order_ids)
        tax_data = self.get_taxes_data(pos_order_ids)
        flexible_tax_data = self.get_flexible_tax_data(pos_order_ids)

        for pos_order in pos_order_ids:
            total_gross_amount += pos_order.amount_total
            total_net_amount += pos_order.margin


        for session_id in mapped_session_ids:
            if session_id.start_at == False:
                raise
            session_ids.append({
                'name':session_id.name,
                'pos_name':session_id.config_id.name,
                'start_date': "In Progress" if session_id.start_at == False else self.get_formated_datetime(session_id.start_at),
                'end_date': "In Progress" if session_id.stop_at == False else self.get_formated_datetime(session_id.stop_at),
            })

        data_list.append({
            'current_date_time':current_date_time,
            'session_ids':session_ids,
            'guest_count':total_guest_count,
            'order_count':total_order_count,
            'payment_data':payment_data,
            'tax_data':tax_data,
            'total_gross_amount':total_gross_amount,
            'total_net_amount':total_net_amount,
            'flexible_tax_data':flexible_tax_data,
        })


        data={
            'datas':data_list
        }

        return data
    
    def get_formated_datetime(self, trans_date):
        trans_date_split = str(trans_date).split('.')[0]
        tz = self.env.user.partner_id.tz and pytz.timezone(self.env.user.partner_id.tz) or pytz.utc
        dt = pytz.utc.localize(datetime.strptime(str(trans_date_split), "%Y-%m-%d %H:%M:%S")).astimezone(tz)
        dt_split = str(str(dt).split('+')[0])
        return dt_split
    
    def get_guest_count_data(self, pos_order_ids):
        total_guest_count = 0
        for pos_order in pos_order_ids:
            total_guest_count += pos_order.customer_count
        return total_guest_count
    
    def get_order_count_data(self, pos_order_ids):
        total_order_count = len(pos_order_ids)
        return total_order_count

    def get_payment_data(self,pos_order_ids):
        payments = []

        # Create a dictionary to store the payment data by payment method
        grouped_payments = defaultdict(lambda: {'count': 0, 'total': 0})

        for pos_order_id in pos_order_ids:
            pos_payment_ids = self.env["pos.payment"].search([('pos_order_id', '=', pos_order_id.id)]).ids
            if pos_payment_ids:
                self.env.cr.execute("""
                    SELECT ppm.name, count(CASE WHEN pp.is_change = 'false' THEN 1 ELSE NULL END) count, sum(amount) total
                    FROM pos_payment AS pp,
                        pos_payment_method AS ppm
                    WHERE pp.payment_method_id = ppm.id
                    AND pp.id IN %s
                    GROUP BY ppm.name;
                """, (tuple(pos_payment_ids),))
                payments = self.env.cr.dictfetchall()
            else:
                payments = []

            for payment in payments:
                for key, value in payment.items():
                    if key == 'name':
                        for k, v in value.items():
                            payment.update({'name':v})
            
            for payment in payments:
                name = payment.get('name')
                count = payment.get('count')
                total = payment.get('total')
                grouped_payments[name]['count'] += count
                grouped_payments[name]['total'] += total
        
        # Convert the grouped payments dictionary to a list
        grouped_payment_data = [{'name': name, 'count': data['count'], 'total': data['total']} for name, data in grouped_payments.items()]
        return grouped_payment_data


    def get_taxes_data(self, pos_order_ids):
        all_orders_taxes_list = []
        for order in pos_order_ids:
            currency = order.pricelist_id.currency_id
            for order_line in order.lines:
                taxes = order_line.tax_ids.filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
                fiscal_position_id = order_line.order_id.fiscal_position_id
                if fiscal_position_id:
                    taxes = fiscal_position_id.map_tax(taxes)
                price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
                taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty, product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
                all_orders_taxes_list.append(taxes)
        
        order_tax_dict_list = []
        for tax_list in all_orders_taxes_list:
            for order_tax in tax_list:
                order_tax_dict_list.append(order_tax)
                
        tax_result = []
        second_result = sorted(order_tax_dict_list,key = itemgetter('name'))
        for key, value in groupby(second_result,key = itemgetter('name')):
            tax_temp_dict = {'name': key}
            total_temp_tax_amount = 0
            for k in value:
                total_temp_tax_amount += k['amount']
            tax_temp_dict.update({'amount': total_temp_tax_amount})
            tax_result.append(tax_temp_dict)
        
        tax_result = sorted(tax_result, key = lambda i: i['name'],reverse=True)
        return tax_result
    

    # My Custom Flexible Tax - Start
    def get_flexible_tax_data(self, pos_order_ids):
        sold_product = {}
        for pos_order in pos_order_ids:
            if pos_order.fiscal_position_id:
                if pos_order.fiscal_position_id.name in sold_product:
                    sold_product[pos_order.fiscal_position_id.name]['qty'] += 1
                    sold_product[pos_order.fiscal_position_id.name]['amount'] += pos_order.amount_paid
                else:
                    sold_product.update({pos_order.fiscal_position_id.name: {'qty': 1, 'amount': pos_order.amount_paid}})
        
        return {
            'products_sold': sold_product,
        }
    
    # My Custom Flexible Tax - End