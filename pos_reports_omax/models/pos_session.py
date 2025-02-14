# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import tz
import pytz
from odoo import fields, models, api, tools
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from collections import Counter
import json
import ast
from itertools import groupby
from operator import itemgetter


class PosConfig(models.Model):
    _inherit = 'pos.config'

    omax_session_pl_report = fields.Boolean(
        string='Session P&L Report ', help='This will allow to print Session P&L Report directly from POS screen')
    omax_session_z_report = fields.Boolean(
        string='Session Z Report ', help='This will allow to print Session Z Report directly from POS screen')
    omax_session_detailed_report = fields.Boolean(
        string='Session Summary Report ', help='This will allow to print Session Report with the POS Order Details, POS Delivery Details and POS Invoice Details directly from POS screen')


class ResConfigZreport(models.TransientModel):
    _inherit = 'res.config.settings'

    omax_session_pl_report = fields.Boolean(
        related='pos_config_id.omax_session_pl_report', readonly=False)
    omax_session_z_report = fields.Boolean(
        related='pos_config_id.omax_session_z_report', readonly=False)
    omax_session_detailed_report = fields.Boolean(
        related='pos_config_id.omax_session_detailed_report', readonly=False)


class PosSession(models.Model):
    _inherit = 'pos.session'

    def action_session_detailed_report(self):
        return self.env.ref('pos_reports_omax.action_report_session_detailed').report_action(self)

    def action_session_pl_report(self):
        return self.env.ref('pos_reports_omax.action_report_session_pl').report_action(self)

    def action_session_z_report(self):
        return self.env.ref('pos_reports_omax.action_report_session_z').report_action(self)

    def get_formated_date(self, datepass):
        formate_date = str(datepass).split('.')[0]
        tz = self.env.user.partner_id.tz and pytz.timezone(
            self.env.user.partner_id.tz) or pytz.utc
        dt = pytz.utc.localize(datetime.strptime(
            str(formate_date), "%Y-%m-%d %H:%M:%S")).astimezone(tz)
        dt_split = str(str(dt).split('+')[0])
        return dt_split

    def get_current_datetime(self):
        now = datetime.now()
        today = str(now).split('.')[0]
        tz = self.env.user.partner_id.tz and pytz.timezone(
            self.env.user.partner_id.tz) or pytz.utc
        dt = pytz.utc.localize(datetime.strptime(
            str(today), "%Y-%m-%d %H:%M:%S")).astimezone(tz)
        dt_split = str(str(dt).split('+')[0])
        return dt_split

    def get_opened_date(self):
        tz = self.env.user.partner_id.tz and pytz.timezone(
            self.env.user.partner_id.tz) or pytz.utc
        dt = pytz.utc.localize(datetime.strptime(
            str(self.start_at), "%Y-%m-%d %H:%M:%S")).astimezone(tz)
        dt_split = str(str(dt).split('+')[0])
        return dt_split

    def get_closed_date(self):
        if self.stop_at:
            tz = self.env.user.partner_id.tz and pytz.timezone(
                self.env.user.partner_id.tz) or pytz.utc
            dt = pytz.utc.localize(datetime.strptime(
                str(self.stop_at), "%Y-%m-%d %H:%M:%S")).astimezone(tz)
            dt_split = str(str(dt).split('+')[0])
            return dt_split

    # My Custom Guest Count - Start
    def get_guest_count_data(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id)])
        total_guest_count = 0
        for pos_order in pos_order_ids:
            total_guest_count += pos_order.customer_count
        return total_guest_count
    # My Custom Guest COunt - End

    # My Custom Flexible Tax - Start
    def get_flexible_tax_data(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id)])
        sold_product = {}
        for pos_order in pos_order_ids:
            if pos_order.fiscal_position_id:
                if pos_order.fiscal_position_id.name in sold_product:
                    sold_product[pos_order.fiscal_position_id.name]['qty'] += 1
                    sold_product[pos_order.fiscal_position_id.name]['amount'] += pos_order.amount_paid
                else:
                    sold_product.update({pos_order.fiscal_position_id.name: {
                                        'qty': 1, 'amount': pos_order.amount_paid}})
        return {
            'products_sold': sold_product,
        }
    # My Custom Flexible Tax - End

    def get_session_amount_data(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id)])
        first_discount_amount = 0.0
        second_discount_amount = 0.0
        discount_amount = 0.0
        taxes_amount = 0.0
        total_sale_amount = 0.0
        total_gross_amount = 0.0
        total_net_amount = 0.0
        total_rounding_amount = 0.0
        total_refund_amount = 0.0
        total_refund_qty = 0.0
        average_bill = 0.0
        average_pax = 0.0
        sold_product = {}
        for pos_order in pos_order_ids:
            currency = pos_order.session_id.currency_id
            total_gross_amount += pos_order.amount_total
            if pos_order.partner_id.name != 'RGM':
                total_net_amount += pos_order.amount_total - pos_order.amount_tax
            total_rounding_amount += pos_order.amount_paid - pos_order.amount_total

            if pos_order.refunded_orders_count > 0:
                total_refund_qty += 1
                for line in pos_order.lines:
                    if line.qty < 0:
                        total_refund_amount += line.price_subtotal_incl

            for line in pos_order.lines:
                if line.product_id.pos_categ_id and line.product_id.pos_categ_id.name and line.product_id.is_discount_product == False:
                    if line.product_id.pos_categ_id.name in sold_product:
                        sold_product[line.product_id.pos_categ_id.name]['qty'] += line.qty
                        sold_product[line.product_id.pos_categ_id.name]['amount'] += line.price_subtotal_incl
                    else:
                        # sold_product.update({line.product_id.pos_categ_id.name: line.qty})
                        sold_product.update({line.product_id.pos_categ_id.name: {
                                            'qty': line.qty, 'amount': line.price_subtotal_incl}})
                # else:
                #     if 'undefine' in sold_product:
                #         sold_product['undefine'] += line.qty
                #     else:
                #         sold_product.update({'undefine': line.qty})
                if line.tax_ids_after_fiscal_position:
                    line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1 - (
                        line.discount or 0.0) / 100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        taxes_amount += tax.get('amount', 0)
                if line.discount > 0:
                    first_discount_amount += -(((line.price_unit *
                                                 line.qty) * line.discount) / 100)
                if line.product_id.is_discount_product == True and line.price_unit < 0:
                    second_discount_amount += line.price_subtotal_incl
                discount_amount = first_discount_amount + second_discount_amount
                if line.product_id.is_discount_product == False:
                    if line.qty > 0 or line.qty < 0:
                        total_sale_amount += line.price_unit * line.qty

        pos_order_count = len(pos_order_ids)
        if pos_order_count > 0:
            average_bill = total_sale_amount / pos_order_count

        guest_count = self.get_guest_count_data()
        if guest_count > 0:
            average_pax = total_sale_amount / self.get_guest_count_data()

        return {
            'total_sale': total_sale_amount,
            'discount': discount_amount,
            'tax': taxes_amount,
            'products_sold': sold_product,
            'total_gross': total_gross_amount - taxes_amount - discount_amount,
            'final_total': total_gross_amount,
            'net_total': total_net_amount,
            'rounding': total_rounding_amount,
            'refund': total_refund_amount,
            'refund_qty': total_refund_qty,
            'average_bill': average_bill,
            'average_pax': average_pax,
        }

# My Custom Product Category Wise Sale - Tax Exclusive - Start
    def get_session_amount_data_tax_exclusive(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id), ('session_id.session_z_product_tax_exclusive', '=', True)])
        sold_product = {}
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id.pos_categ_id and line.product_id.pos_categ_id.name and line.product_id.is_discount_product == False:
                    if line.product_id.pos_categ_id.name in sold_product:
                        sold_product[line.product_id.pos_categ_id.name]['qty'] += line.qty
                        sold_product[line.product_id.pos_categ_id.name]['amount'] += line.price_subtotal
                    else:
                        sold_product.update({line.product_id.pos_categ_id.name: {
                                            'qty': line.qty, 'amount': line.price_subtotal}})
        return {
            'products_sold': sold_product,
        }
# My Custom Product Category Wise Sale - Tax Exclusive - End

    # My Custom Product Wise Sale - Start
    def get_session_detail_product_amount_data(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id), ('session_id.session_z_product', '=', True)])
        sold_product = {}
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id and line.product_id.name and line.product_id.is_discount_product == False:
                    if line.product_id.name in sold_product:
                        sold_product[line.product_id.name]['qty'] += line.qty
                        sold_product[line.product_id.name]['amount'] += line.price_subtotal_incl
                        sold_product[line.product_id.name]['barcode'] = line.product_id.barcode
                    else:
                        sold_product.update(
                            {line.product_id.name: {'qty': line.qty, 'amount': line.price_subtotal_incl, 'barcode': line.product_id.barcode}})
                if line.product_id and line.product_id.name and line.product_id.is_pack == True:
                    for combo_product in line.combo_prod_ids:
                        if combo_product.name in sold_product:
                            sold_product[combo_product.name]['qty'] += line.qty
                            # sold_product[combo_product.name]['amount'] += line.price_subtotal_incl
                        else:
                            sold_product.update(
                                {combo_product.name: {'qty': line.qty, 'amount': 0, 'barcode': line.product_id.barcode}})
                # else:
                #     if 'undefine' in sold_product:
                #         sold_product['undefine'] += line.qty
                #     else:
                #         sold_product.update({'undefine': line.qty})
        return {
            'products_sold': sold_product,
        }
    # My Custom Product Wise Sale - End

    # My Custom Product Wise Sale - Tax Exclusive- Start

    def get_session_detail_product_tax_exclusive_amount_data(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id), ('session_id.session_z_product_tax_exclusive', '=', True)])
        sold_product = {}
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id and line.product_id.name and line.product_id.is_discount_product == False:
                    if line.product_id.name in sold_product:
                        sold_product[line.product_id.name]['qty'] += line.qty
                        sold_product[line.product_id.name]['amount'] += line.price_subtotal
                        sold_product[line.product_id.name]['barcode'] = line.product_id.barcode
                    else:
                        sold_product.update(
                            {line.product_id.name: {'qty': line.qty, 'amount': line.price_subtotal, 'barcode': line.product_id.barcode}})
                if line.product_id and line.product_id.name and line.product_id.is_pack == True:
                    for combo_product in line.combo_prod_ids:
                        if combo_product.name in sold_product:
                            sold_product[combo_product.name]['qty'] += line.qty
                        else:
                            sold_product.update(
                                {combo_product.name: {'qty': line.qty, 'amount': 0, 'barcode': line.product_id.barcode}})
        return {
            'products_sold': sold_product,
        }
    # My Custom Product Wise Sale - Tax Exclusive- End


# My Custom Discount Wise Sale - Start

    def get_session_discount_amount_data(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id)])
        sold_product = {}
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id and line.product_id.name and line.product_id.is_discount_product == True and line.product_id.is_discount_label == False:
                    if line.full_product_name in sold_product:
                        sold_product[line.full_product_name]['qty'] += line.qty
                        sold_product[line.full_product_name]['amount'] += line.price_subtotal_incl
                    else:
                        sold_product.update(
                            {line.full_product_name: {'qty': line.qty, 'amount': line.price_subtotal_incl}})
                elif line.product_id and line.product_id.name and line.discount > 0:
                    if str(int(line.discount)) + '% on your order' in sold_product:
                        sold_product[str(int(line.discount)) +
                                     '% on your order']['qty'] += line.qty
                        sold_product[str(
                            int(line.discount)) + '% on your order']['amount'] += -(((line.price_unit * line.qty) * line.discount) / 100)
                    else:
                        sold_product.update({str(int(line.discount)) + '% on your order': {
                                            'qty': line.qty, 'amount': -(((line.price_unit * line.qty) * line.discount) / 100)}})
                # else:
                #     if 'undefine' in sold_product:
                #         sold_product['undefine']['qty'] += line.qty
                #         sold_product['undefine']['amount'] += line.price_subtotal_incl
                #     else:
                #         sold_product.update({'undefine': {'qty': line.qty, 'amount': line.price_subtotal_incl}})

        return {
            'products_sold': sold_product,
        }
    # My Custom Discount Wise Sale - End

    def get_taxes_data(self):
        order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id)])
        all_orders_taxes_list = []
        for order in order_ids:
            currency = order.pricelist_id.currency_id
            for order_line in order.lines:
                taxes = order_line.tax_ids.filtered(
                    lambda t: t.company_id.id == order_line.order_id.company_id.id)
                fiscal_position_id = order_line.order_id.fiscal_position_id
                if fiscal_position_id:
                    taxes = fiscal_position_id.map_tax(taxes)
                price = order_line.price_unit * \
                    (1 - (order_line.discount or 0.0) / 100.0)
                taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty,
                                          product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
                all_orders_taxes_list.append(taxes)

        order_tax_dict_list = []
        for tax_list in all_orders_taxes_list:
            for order_tax in tax_list:
                order_tax_dict_list.append(order_tax)

        tax_result = []
        second_result = sorted(order_tax_dict_list, key=itemgetter('name'))
        for key, value in groupby(second_result, key=itemgetter('name')):
            tax_temp_dict = {'name': key}
            total_temp_tax_amount = 0
            for k in value:
                total_temp_tax_amount += k['amount']
            tax_temp_dict.update({'amount': total_temp_tax_amount})
            tax_result.append(tax_temp_dict)

        tax_result = sorted(tax_result, key=lambda i: i['name'], reverse=True)
        return tax_result

    def get_pricelist(self):
        pos_order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id)])
        pricelist = {}
        for pos_order in pos_order_ids:
            if pos_order.pricelist_id.name:
                if pos_order.pricelist_id.name in pricelist:
                    pricelist[pos_order.pricelist_id.name] += pos_order.amount_total
                else:
                    pricelist.update(
                        {pos_order.pricelist_id.name: pos_order.amount_total})
            else:
                if 'undefine' in pricelist:
                    pricelist['undefine'] += pos_order.amount_total
                else:
                    pricelist.update({'undefine': pos_order.amount_total})
        return pricelist

    def get_pricelist_qty(self, pricelist):
        if pricelist:
            qty_pricelist = 0
            pricelist_obj = self.env['product.pricelist'].search(
                [('name', '=', str(pricelist))])
            if pricelist_obj:
                pos_order_ids = self.env['pos.order'].search(
                    [('session_id', '=', self.id), ('pricelist_id.id', '=', pricelist_obj.id)])
                qty_pricelist = len(pos_order_ids)
            else:
                if pricelist == 'undefine':
                    pos_order_ids = self.env['pos.order'].search(
                        [('session_id', '=', self.id), ('pricelist_id', '=', False)])
                    qty_pricelist = len(pos_order_ids)
            return int(qty_pricelist)

    def get_payment_data(self):
        pos_payment_ids = self.env["pos.payment"].search(
            [('session_id', '=', self.id)]).ids
        if pos_payment_ids:
            self.env.cr.execute("""
                SELECT ppm.name, count(CASE WHEN pp.is_change = 'false' THEN 1 ELSE NULL END) count, sum(currency_amount_total) total, pp.selected_currency_symbol, sum(amount) amount_total
                FROM pos_payment AS pp,
                     pos_payment_method AS ppm
                WHERE pp.payment_method_id = ppm.id
                AND pp.id IN %s
                GROUP BY ppm.name, pp.selected_currency_symbol;
            """, (tuple(pos_payment_ids),))
            payments = self.env.cr.dictfetchall()
        else:
            payments = []

        for payment in payments:
            for key, value in payment.items():
                if key == 'name':
                    for k, v in value.items():
                        payment.update({'name': v})
        return payments

    def get_payment_qty(self, payment_method):
        qty_payment_method = 0
        if payment_method:
            orders = self.env['pos.order'].search(
                [('session_id', '=', self.id)])
            st_line_obj = self.env["account.bank.statement.line"].search(
                [('pos_statement_id', 'in', orders.ids)])
            if len(st_line_obj) > 0:
                res = []
                for line in st_line_obj:
                    res.append(line.journal_id.name)
                res_dict = ast.literal_eval(json.dumps(dict(Counter(res))))
                if payment_method in res_dict:
                    qty_payment_method = res_dict[payment_method]
        return int(qty_payment_method)

    def get_pos_orders(self):
        order_ids = self.env['pos.order'].search(
            [('session_id', '=', self.id)])
        return order_ids

    def get_pickings(self):
        pickings = []
        for pos in self:
            pickings = pos.picking_ids
            return pickings

    def get_session_payments(self):
        for pos in self:
            payment_ids = pos.order_ids.mapped('payment_ids')
            return payment_ids

    def get_session_invoices(self):
        invoice_ids = []
        for pos in self:
            for order in pos.order_ids:
                move_id = self.env['account.move'].search(
                    [('invoice_origin', '=', order.name)], limit=1)
                if move_id:
                    invoice_ids.append(move_id)
        return invoice_ids

    def _loader_params_res_company(self):
        return {
            'search_params': {
                'domain': [('id', '=', self.company_id.id)],
                'fields': [
                    'street', 'street2', 'city', 'zip',
                    'currency_id', 'email', 'website', 'company_registry', 'vat', 'name', 'phone', 'partner_id',
                    'country_id', 'state_id', 'tax_calculation_rounding_method', 'nomenclature_id', 'point_of_sale_use_ticket_qr_code',
                ],
            }
        }

    # for report only

    def get_diff_valaue_of_close_session(self):
        message = self.env['mail.message'].sudo().search(
            [('model', '=', 'pos.session'), ('res_id', '=', self.id)])
        for msg in message:
            plaintext = tools.html_to_inner_content(msg.body)  # html to text
            # print(plaintext,type(plaintext))
            if 'Closing difference:' in plaintext:
                plaintext_lst = plaintext.split(' ')
                # print("plaintext_lst[-1]===>>",plaintext_lst[-1])
                if self.currency_id.position == 'before':
                    if plaintext_lst:
                        return float(plaintext_lst[-1])
                if self.currency_id.position == 'after':
                    plaintext_lst.pop(-1)
                    # print("plaintext_lst==>>",plaintext_lst)
                    if plaintext_lst:
                        return float(plaintext_lst[-1])
        return 0.0
