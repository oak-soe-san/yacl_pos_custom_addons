from odoo import _, api, fields, models
from datetime import datetime, timedelta
import pytz


class MonthlySaleReportWizard(models.TransientModel):
    _name = 'monthly.sale.report.wizard'
    _description = 'Monthly Sale Report Wizard'

    date_from = fields.Datetime(string='Start From', required=True)
    date_to = fields.Datetime(string='End To', required=True)
    issued_date = fields.Datetime(string='Issued Date', default=datetime.now())
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    def action_print_report(self):
        start_date = self.date_from
        end_date = self.date_to
        issued_date = self.issued_date
        company_name = self.company_id.name

        _domain = [('date_order', '>=', start_date),
                   ('date_order', '<=', end_date)]

        pos_order_records = self.env['pos.order'].search(_domain)

        data = {}
        data['order_data'] = self._get_pos_orders(pos_order_records)
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['issued_date'] = issued_date
        data['company_name'] = company_name

        return self.env.ref('pos_management_system.monthly_sale_report_action').report_action(self, data=data)

    def convert_time_zone(self, trans_date):
        tz = self.env.user.partner_id.tz and pytz.timezone(
            self.env.user.partner_id.tz) or pytz.utc
        localized_order_date = pytz.utc.localize(datetime.strptime(
            str(trans_date), "%Y-%m-%d %H:%M:%S")).astimezone(tz)
        return localized_order_date

    def _get_pos_orders(self, pos_order_records):

        sold_product = {}

        for order_record in pos_order_records:
            order_date = self.convert_time_zone(
                order_record.date_order).strftime('%Y-%m-%d')

            if order_record.date_order and order_date and order_record.partner_id.name != 'RGM':
                if order_date in sold_product:
                    sold_product[order_date]['tax'] += order_record.amount_tax
                    sold_product[order_date]['margin'] += order_record.amount_total - order_record.amount_tax
                    sold_product[order_date]['amount_paid'] += order_record.amount_total
                    sold_product[order_date]['order_count'] = order_record.session_id.order_count
                    sold_product[order_date]['rounding_amount'] += order_record.amount_paid - \
                        order_record.amount_total

                    for line in order_record.lines:
                        if line.discount > 0:
                            first_discount_amount += -(((line.price_unit *
                                                         line.qty) * line.discount) / 100)
                            discount_trans_count += 1
                        if line.product_id.is_discount_product == True and line.price_unit < 0:
                            second_discount_amount += line.price_subtotal_incl
                            discount_trans_count += 1

                    discount_amount = first_discount_amount + second_discount_amount
                    discount_trans_count = discount_trans_count

                    sold_product[order_date]['discount_amount'] = discount_amount
                    sold_product[order_date]['discount_trans_count'] = discount_trans_count

                else:
                    discount_amount = 0.0
                    first_discount_amount = 0.0
                    second_discount_amount = 0.0
                    discount_trans_count = 0.0

                    for line in order_record.lines:
                        if line.discount > 0:
                            first_discount_amount += -(((line.price_unit *
                                                         line.qty) * line.discount) / 100)
                            discount_trans_count += 1
                        if line.product_id.is_discount_product == True and line.price_unit < 0:
                            second_discount_amount += line.price_subtotal_incl
                            discount_trans_count += 1

                    discount_amount = first_discount_amount + second_discount_amount
                    discount_trans_count = discount_trans_count

                    sold_product.update({order_date: {
                                        'tax': order_record.amount_tax, 'margin': order_record.amount_total - order_record.amount_tax, 'amount_paid': order_record.amount_total,
                                        'order_count': order_record.session_id.order_count, 'rounding_amount': order_record.amount_paid - order_record.amount_total,
                                        'discount_amount': discount_amount, 'discount_trans_count': discount_trans_count}})

        sold_product = dict(sorted(sold_product.items()))

        data = {
            'datas': sold_product,
        }

        return data
