from odoo import models, fields, api, _
from odoo.osv.expression import AND

class ReportSaleDetails(models.AbstractModel):

    _inherit = 'report.point_of_sale.report_saledetails'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = super()._get_report_values(docids, data)

        for product in data['products']:
            product_id = product['product_id']
            product_obj = self.env['product.product'].browse(product_id)
            product['is_pack'] = product_obj.is_pack

        products_list = data.get('products', [])
        sorted_products_list = sorted(products_list, key=lambda x: (x["price_unit"] == 0, x["price_unit"]))
        unique_products_dict = {}

        for product in sorted_products_list:
            product_name = product.get('product_name', '')
            if product_name not in unique_products_dict:
                unique_products_dict[product_name] = product
            else:
                unique_products_dict[product_name]['quantity'] += product['quantity']

        unique_products = list(unique_products_dict.values())
        data['products'] = unique_products

        # E Wallet Tax Remove
        date_start = data['date_start']
        date_stop = data['date_stop']
        config_ids = self.env['pos.config'].browse(data['config_ids']).ids
        session_ids = data['session_ids']

        domain = [('state', 'in', ['paid','invoiced','done'])]

        if (session_ids):
            domain = AND([domain, [('session_id', 'in', session_ids)]])
        else:
            if date_start:
                date_start = fields.Datetime.from_string(date_start)
            else:
                # start by default today 00:00:00
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
                today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
                date_start = today.astimezone(pytz.timezone('UTC'))

            if date_stop:
                date_stop = fields.Datetime.from_string(date_stop)
                # avoid a date_stop smaller than date_start
                if (date_stop < date_start):
                    date_stop = date_start + timedelta(days=1, seconds=-1)
            else:
                # stop by default today 23:59:59
                date_stop = date_start + timedelta(days=1, seconds=-1)

            domain = AND([domain,
                [('date_order', '>=', fields.Datetime.to_string(date_start)),
                ('date_order', '<=', fields.Datetime.to_string(date_stop))]
            ])

            if config_ids:
                domain = AND([domain, [('config_id', 'in', config_ids)]])

        orders = self.env['pos.order'].search(domain)

        taxes = {}
        for order in orders:
            currency = order.session_id.currency_id

            for line in order.lines:

                config_id = self.env['pos.config'].browse(data['config_ids'])
                if config_id.is_global_discount_tax_exclusive:
                    
                    if line.tax_ids_after_fiscal_position:
                        if not line.is_reward_line and not line.product_id.is_discount_product and line.order_id.amount_total != 0:
                            line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1 - (line.discount or 0.0) / 100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                            #taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty, product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
                            for custom_tax in line_taxes['taxes']:
                                taxes.setdefault(custom_tax['id'], {'name': custom_tax['name'], 'tax_amount':0.0, 'base_amount':0.0})
                                if line.tax_ids.amount_type == 'fixed':
                                    taxes[custom_tax['id']]['tax_amount'] += custom_tax['amount']
                                    taxes[custom_tax['id']]['base_amount'] += custom_tax['base']
                                else:
                                    taxes[custom_tax['id']]['tax_amount'] += (custom_tax['base'] - (custom_tax['base'] * line.global_discount_percentage/100)) * line.tax_ids_after_fiscal_position.amount/100
                                    taxes[custom_tax['id']]['base_amount'] += custom_tax['base']
                    else:
                        taxes.setdefault(0, {'name': _('No Taxes'), 'tax_amount':0.0, 'base_amount':0.0})

                    data.update({'taxes': list(taxes.values())})

        return data