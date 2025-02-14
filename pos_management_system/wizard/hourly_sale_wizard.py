from odoo import _, api, fields, models
from datetime import datetime, timedelta
import pytz


class HourlySaleReportWizard(models.TransientModel):
    _name = 'hourly.sale.report.wizard'
    _description = 'Hourly Sale Report Wizard'

    employee_id = fields.Many2one('hr.employee', string="Employee", widget='many2one', placeholder="Shops that are using Employee Information")
    user_id = fields.Many2one('res.users', string="User", placeholder="Shops that are using User Account Information")
    session_id = fields.Many2one('pos.session', string="Session")
    date_from = fields.Datetime(string='Start From', required=True)
    date_to = fields.Datetime(string='End To', required=True)

    def action_print_report(self):
        start_date = self.date_from
        end_date = self.date_to
        
        _domain = [('date_order', '>=', start_date),('date_order', '<=', end_date)]
        
        if self.employee_id:
            _domain.append(('employee_id', '=', self.employee_id.id))
        if self.user_id:
            _domain.append(('user_id', '=', self.user_id.id))
        if self.session_id:
            _domain.append(('session_id', '=', self.session_id.id))    
        
        pos_order_ids = self.env['pos.order'].search(_domain)
        
        data = {}
        data['pos_orders'] = self._get_pos_orders(pos_order_ids)
        data['start_date'] = self.convert_time_zone(start_date)
        data['end_date'] = self.convert_time_zone(end_date)
        data['employee_id'] = self.employee_id.name
        data['user_id'] = self.user_id.name
        data['session_id'] = self.session_id.name
        data['report_date'] = self.get_current_datetime()

        return self.env.ref('pos_management_system.hourly_sale_report_action').report_action(self,data=data)
    
    def get_current_datetime(self):
        now = datetime.now()
        today = str(now).split('.')[0]
        dt = self.convert_time_zone(today)
        dt_split = str(str(dt).split('+')[0])
        return dt_split
    
    def convert_time_zone(self,trans_date):
        tz = self.env.user.partner_id.tz and pytz.timezone(self.env.user.partner_id.tz) or pytz.utc
        localized_order_date = pytz.utc.localize(datetime.strptime(str(trans_date), "%Y-%m-%d %H:%M:%S")).astimezone(tz)
        return localized_order_date
    
    def get_round_down_hour(self,order_date):
        localized_order_date = self.convert_time_zone(order_date)
        rounded_hour = localized_order_date.replace(minute=0, second=0, microsecond=0)
        rounded_hour = rounded_hour.strftime("%H:%M")
        return rounded_hour
    
    def _get_pos_orders(self,pos_order_ids):
        hourly_orders = {}
        for order in pos_order_ids:
            order_date = order.date_order
            hour = self.get_round_down_hour(order_date)
            hour_obj = datetime.strptime(hour, '%H:%M')
            next_hour_obj = hour_obj + timedelta(hours=1)
            next_hour = next_hour_obj.strftime('%H:%M')
            if hour in hourly_orders:
                hourly_orders[hour]['count'] += 1
                hourly_orders[hour]['sale_amount'] += order.amount_paid
            else:
                hourly_orders[hour] = {
                    'count':1,
                    'sale_amount': order.amount_paid,
                    'next_hour': next_hour,
                }
        
        sorted_hourly_orders = dict(sorted(hourly_orders.items(), key=lambda x: x[0]))
        
        return sorted_hourly_orders