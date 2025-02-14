# -*- coding: utf-8 -*-
from odoo import fields, models, api, tools
import json
from operator import itemgetter
from itertools import groupby

class PosSession(models.Model):
    _inherit = 'pos.session'

    # ORIGINAL BEFORE ORVERRIDE

    # def get_session_detail_product_amount_data(self):
    #     pos_order_ids = self.env['pos.order'].search(
    #         [('session_id', '=', self.id), ('session_id.session_z_product', '=', True)])
    #     sold_product = {}
    #     for pos_order in pos_order_ids:
    #         for line in pos_order.lines:
    #             if line.product_id and line.product_id.name and line.product_id.is_discount_product == False:
    #                 if line.product_id.name in sold_product:
    #                     sold_product[line.product_id.name]['qty'] += line.qty
    #                     sold_product[line.product_id.name]['amount'] += line.price_subtotal_incl
    #                     sold_product[line.product_id.name]['barcode'] = line.product_id.barcode
    #                 else:
    #                     sold_product.update(
    #                         {line.product_id.name: {'qty': line.qty, 'amount': line.price_subtotal_incl, 'barcode': line.product_id.barcode}})
    #             if line.product_id and line.product_id.name and line.product_id.is_pack == True:
    #                 for combo_product in line.combo_prod_ids:
    #                     if combo_product.name in sold_product:
    #                         sold_product[combo_product.name]['qty'] += line.qty
    #                         # sold_product[combo_product.name]['amount'] += line.price_subtotal_incl
    #                     else:
    #                         sold_product.update(
    #                             {combo_product.name: {'qty': line.qty, 'amount': 0, 'barcode': line.product_id.barcode}})
    #             # else:
    #             #     if 'undefine' in sold_product:
    #             #         sold_product['undefine'] += line.qty
    #             #     else:
    #             #         sold_product.update({'undefine': line.qty})
    #     return {
    #         'products_sold': sold_product,
    #     }

    # 3 OVERRIDE

    def get_session_detail_product_amount_data(self):
        pos_order_ids = self.env['pos.order'].search([('session_id', '=', self.id),('session_id.session_z_product', '=', True)])
        sold_product = {}
        combo_sold_product = {}
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id and line.product_id.name and line.product_id.is_discount_product == False:
                    if line.product_id.name in sold_product:

                        # 1 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE AND COMBO
                        if self.config_id.is_global_discount_tax_exclusive or self.config_id.use_combo:
                            if self.config_id.use_combo:
                                if line.product_id.is_pack == False:
                                    sold_product[line.product_id.name]['qty'] += line.qty
                                    sold_product[line.product_id.name]['amount'] += line.price_subtotal
                                    sold_product[line.product_id.name]['barcode'] = line.product_id.barcode
                            elif self.config_id.is_global_discount_tax_exclusive:
                                sold_product[line.product_id.name]['qty'] += line.qty
                                sold_product[line.product_id.name]['amount'] += line.price_subtotal
                                sold_product[line.product_id.name]['barcode'] = line.product_id.barcode
                        else:
                            sold_product[line.product_id.name]['qty'] += line.qty
                            sold_product[line.product_id.name]['amount'] += line.price_subtotal_incl
                            sold_product[line.product_id.name]['barcode'] = line.product_id.barcode
                        #

                    else:

                        # 2 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE AND COMBO
                        if self.config_id.is_global_discount_tax_exclusive or self.config_id.use_combo:
                            if self.config_id.use_combo:
                                if line.product_id.is_pack == False:
                                    sold_product.update({line.product_id.name: {'qty': line.qty, 'amount': line.price_subtotal, 'barcode': line.product_id.barcode}})
                            elif self.config_id.is_global_discount_tax_exclusive:
                                sold_product.update({line.product_id.name: {'qty': line.qty, 'amount': line.price_subtotal, 'barcode': line.product_id.barcode}})
                        else:
                            sold_product.update({line.product_id.name: {'qty': line.qty, 'amount': line.price_subtotal_incl, 'barcode': line.product_id.barcode}})
                        #
                
        # 3 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE AND COMBO
        
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id.name in sold_product:
                    if sold_product[line.product_id.name]['qty'] == 0:
                        del sold_product[line.product_id.name]

        if self.config_id.use_combo:
            sorted_sold_product = dict(sorted(sold_product.items(), key=lambda item: item[1]['amount'] == 0))
            sold_product = sorted_sold_product
        #
                
        # else:
        #     if 'undefine' in sold_product:
        #         sold_product['undefine'] += line.qty
        #     else:
        #         sold_product.update({'undefine': line.qty})

        return {
            'products_sold': sold_product,
        }

    # NEW METHOD

    # KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE AND COMBO
    def get_session_detail_combo_product_amount_data(self):
        pos_order_ids = self.env['pos.order'].search([('session_id', '=', self.id),('session_id.session_z_product', '=', True)])
        sold_product = {}
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id and line.product_id.name and line.product_id.is_discount_product == False:

                    if line.product_id.name in sold_product:
                        if line.product_id.is_pack:
                            sold_product[line.product_id.name]['qty'] += line.qty
                            sold_product[line.product_id.name]['amount'] += line.price_subtotal
                    elif line.product_id.is_pack:
                        sold_product.update({line.product_id.name: {'qty': line.qty, 'amount': line.price_subtotal}})

        for pos_order in pos_order_ids:
            for line in pos_order.lines:  
                if line.product_id.name in sold_product:
                    if sold_product[line.product_id.name]['qty'] == 0:
                        del sold_product[line.product_id.name]

        return {
            'products_sold': sold_product,
        }
        #

    # ORIGINAL BEFORE ORVERRIDE

    # def get_session_discount_amount_data(self):
    #     pos_order_ids = self.env['pos.order'].search(
    #         [('session_id', '=', self.id)])
    #     sold_product = {}
    #     for pos_order in pos_order_ids:
    #         for line in pos_order.lines:
    #             if line.product_id and line.product_id.name and line.product_id.is_discount_product == True and line.product_id.is_discount_label == False:
    #                 if line.full_product_name in sold_product:
    #                     sold_product[line.full_product_name]['qty'] += line.qty
    #                     sold_product[line.full_product_name]['amount'] += line.price_subtotal_incl
    #                 else:
    #                     sold_product.update(
    #                         {line.full_product_name: {'qty': line.qty, 'amount': line.price_subtotal_incl}})
    #             elif line.product_id and line.product_id.name and line.discount > 0:
    #                 if str(int(line.discount)) + '% on your order' in sold_product:
    #                     sold_product[str(int(line.discount)) +
    #                                  '% on your order']['qty'] += line.qty
    #                     sold_product[str(
    #                         int(line.discount)) + '% on your order']['amount'] += -(((line.price_unit * line.qty) * line.discount) / 100)
    #                 else:
    #                     sold_product.update({str(int(line.discount)) + '% on your order': {
    #                                         'qty': line.qty, 'amount': -(((line.price_unit * line.qty) * line.discount) / 100)}})
    #             # else:
    #             #     if 'undefine' in sold_product:
    #             #         sold_product['undefine']['qty'] += line.qty
    #             #         sold_product['undefine']['amount'] += line.price_subtotal_incl
    #             #     else:
    #             #         sold_product.update({'undefine': {'qty': line.qty, 'amount': line.price_subtotal_incl}})

    #     return {
    #         'products_sold': sold_product,
    #     }

    # 1 OVERRIDE

    def get_session_discount_amount_data(self):
        pos_order_ids = self.env['pos.order'].search([('session_id', '=', self.id)])
        sold_product = {}
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id and line.product_id.name and line.product_id.is_discount_product == True and line.product_id.is_discount_label == False:
                    if line.full_product_name in sold_product:
                        sold_product[line.full_product_name]['qty'] += line.qty
                        sold_product[line.full_product_name]['amount'] += line.price_subtotal_incl
                    else:

                        # 1 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE
                        if self.config_id.is_global_discount_tax_exclusive:
                            sold_product.update({line.full_product_name: {'qty': line.qty, 'amount': line.price_subtotal}})
                        else:
                            sold_product.update({line.full_product_name: {'qty': line.qty, 'amount': line.price_subtotal_incl}})
                        #

                elif line.product_id and line.product_id.name and line.discount > 0:
                    if str(int(line.discount)) + '% on your order' in sold_product:
                        sold_product[str(int(line.discount)) + '% on your order']['qty'] += line.qty
                        sold_product[str(int(line.discount)) + '% on your order']['amount'] += -(((line.price_unit * line.qty) * line.discount) / 100)
                    else:
                        sold_product.update({str(int(line.discount)) + '% on your order': {'qty': line.qty, 'amount': -(((line.price_unit * line.qty) * line.discount) / 100)}})
                # else:
                #     if 'undefine' in sold_product:
                #         sold_product['undefine']['qty'] += line.qty
                #         sold_product['undefine']['amount'] += line.price_subtotal_incl
                #     else:
                #         sold_product.update({'undefine': {'qty': line.qty, 'amount': line.price_subtotal_incl}})

        return {
            'products_sold': sold_product,
        }

    # ORIGINAL BEFORE ORVERRIDE

    # def get_taxes_data(self):
    #     order_ids = self.env['pos.order'].search([('session_id', '=', self.id)])
    #     all_orders_taxes_list = []
    #     for order in order_ids:
    #         currency = order.pricelist_id.currency_id
    #         for order_line in order.lines:
    #             taxes = order_line.tax_ids.filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
    #             fiscal_position_id = order_line.order_id.fiscal_position_id
    #             if fiscal_position_id:
    #                 taxes = fiscal_position_id.map_tax(taxes)
    #             price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
    #             taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty, product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
    #             all_orders_taxes_list.append(taxes)
        
    #     order_tax_dict_list = []
    #     for tax_list in all_orders_taxes_list:
    #         for order_tax in tax_list:
    #             order_tax_dict_list.append(order_tax)
                
    #     tax_result = []
    #     second_result = sorted(order_tax_dict_list,key = itemgetter('name'))
    #     for key, value in groupby(second_result,key = itemgetter('name')):
    #         tax_temp_dict = {'name': key}
    #         total_temp_tax_amount = 0
    #         for k in value:
    #             total_temp_tax_amount += k['amount']
    #         tax_temp_dict.update({'amount': total_temp_tax_amount})
    #         tax_result.append(tax_temp_dict)
        
    #     tax_result = sorted(tax_result, key = lambda i: i['name'],reverse=True)
    #     return tax_result
    
    # 1 OVERRIDE

    def get_taxes_data(self):
        order_ids = self.env['pos.order'].search([('session_id', '=', self.id)])
        all_orders_taxes_list = []
        for order in order_ids:
            currency = order.pricelist_id.currency_id
            for order_line in order.lines:
                taxes = order_line.tax_ids.filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
                fiscal_position_id = order_line.order_id.fiscal_position_id
                if fiscal_position_id:
                    taxes = fiscal_position_id.map_tax(taxes)
                price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)

                 # 1 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE
                if self.config_id.is_global_discount_tax_exclusive:
                    amount = taxes.amount
                    if not order_line.is_reward_line and not order_line.product_id.is_discount_product:
                        taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty, product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
                        if order_line.tax_ids.amount_type == 'fixed':
                            pass
                        else:
                            for custom_tax in taxes:
                                custom_tax['amount'] = (custom_tax['base'] - (custom_tax['base'] * order_line.global_discount_percentage/100)) * amount/100
                    if type(taxes) is list and order.amount_total != 0.0:
                        all_orders_taxes_list.append(taxes)
                else:
                    taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty, product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
                    all_orders_taxes_list.append(taxes)
                #
        
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

    # ORIGINAL BEFORE ORVERRIDE

    # def get_session_amount_data(self):
    #     pos_order_ids = self.env['pos.order'].search(
    #         [('session_id', '=', self.id)])
    #     first_discount_amount = 0.0
    #     second_discount_amount = 0.0
    #     discount_amount = 0.0
    #     taxes_amount = 0.0
    #     total_sale_amount = 0.0
    #     total_gross_amount = 0.0
    #     total_net_amount = 0.0
    #     total_rounding_amount = 0.0
    #     total_refund_amount = 0.0
    #     total_refund_qty = 0.0
    #     average_bill = 0.0
    #     average_pax = 0.0
    #     sold_product = {}
    #     for pos_order in pos_order_ids:
    #         currency = pos_order.session_id.currency_id
    #         total_gross_amount += pos_order.amount_total
    #         if pos_order.partner_id.name != 'RGM':
    #           total_net_amount += pos_order.margin
    #         total_rounding_amount += pos_order.amount_paid - pos_order.amount_total

    #         if pos_order.refunded_orders_count > 0:
    #             total_refund_qty += 1
    #             for line in pos_order.lines:
    #                 if line.qty < 0:
    #                     total_refund_amount += line.price_subtotal_incl

    #         for line in pos_order.lines:
    #             if line.product_id.pos_categ_id and line.product_id.pos_categ_id.name and line.product_id.is_discount_product == False:
    #                 if line.product_id.pos_categ_id.name in sold_product:
    #                     sold_product[line.product_id.pos_categ_id.name]['qty'] += line.qty
    #                     sold_product[line.product_id.pos_categ_id.name]['amount'] += line.price_subtotal_incl
    #                 else:
    #                     # sold_product.update({line.product_id.pos_categ_id.name: line.qty})
    #                     sold_product.update({line.product_id.pos_categ_id.name: {
    #                                         'qty': line.qty, 'amount': line.price_subtotal_incl}})
    #             # else:
    #             #     if 'undefine' in sold_product:
    #             #         sold_product['undefine'] += line.qty
    #             #     else:
    #             #         sold_product.update({'undefine': line.qty})
    #             if line.tax_ids_after_fiscal_position:
    #                 line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1 - (
    #                     line.discount or 0.0) / 100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
    #                 for tax in line_taxes['taxes']:
    #                     taxes_amount += tax.get('amount', 0)
    #             if line.discount > 0:
    #                 first_discount_amount += -(((line.price_unit *
    #                                             line.qty) * line.discount) / 100)
    #             if line.product_id.is_discount_product == True and line.price_unit < 0:
    #                 second_discount_amount += line.price_subtotal_incl
    #             discount_amount = first_discount_amount + second_discount_amount
    #             if line.product_id.is_discount_product == False:
    #                 if line.qty > 0 or line.qty < 0:
    #                     total_sale_amount += line.price_unit * line.qty

    #     pos_order_count = len(pos_order_ids)
    #     if pos_order_count > 0:
    #         average_bill = total_sale_amount / pos_order_count

    #     guest_count = self.get_guest_count_data()
    #     if guest_count > 0:
    #         average_pax = total_sale_amount / self.get_guest_count_data()

    #     return {
    #         'total_sale': total_sale_amount,
    #         'discount': discount_amount,
    #         'tax': taxes_amount,
    #         'products_sold': sold_product,
    #         'total_gross': total_gross_amount - taxes_amount - discount_amount,
    #         'final_total': total_gross_amount,
    #         'net_total': total_net_amount,
    #         'rounding': total_rounding_amount,
    #         'refund': total_refund_amount,
    #         'refund_qty': total_refund_qty,
    #         'average_bill': average_bill,
    #         'average_pax': average_pax,
    #     }

    # 5 OVERRIDE

    def get_session_amount_data(self):
        pos_order_ids = self.env['pos.order'].search([('session_id', '=', self.id)])
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
                        # 1 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE
                        if self.config_id.is_global_discount_tax_exclusive:
                            if line.for_refund_price > 0:
                                total_refund_amount += line.for_refund_price
                            else:
                                total_refund_amount += line.price_subtotal_incl
                        else:
                            total_refund_amount += line.price_subtotal_incl
                        #

            for line in pos_order.lines:
                if line.product_id.pos_categ_id and line.product_id.pos_categ_id.name and line.product_id.is_discount_product == False:
                    if line.product_id.pos_categ_id.name in sold_product:
                        sold_product[line.product_id.pos_categ_id.name]['qty'] += line.qty
                        sold_product[line.product_id.pos_categ_id.name]['amount'] += line.price_subtotal_incl
                    else:
                        # sold_product.update({line.product_id.pos_categ_id.name: line.qty})
                        sold_product.update({line.product_id.pos_categ_id.name: {'qty': line.qty, 'amount': line.price_subtotal_incl}})
                # else:
                #     if 'undefine' in sold_product:
                #         sold_product['undefine'] += line.qty
                #     else:
                #         sold_product.update({'undefine': line.qty})

                # 2 KN CUSTOMIZATION FOR COMBO 
                if self.config_id.use_combo:
                    if line.product_id.is_pack == True:
                        if line.product_id.pos_categ_id.name in sold_product:
                            sold_product[line.product_id.pos_categ_id.name]['qty'] -= line.qty
                #

                if line.tax_ids_after_fiscal_position:

                    # 3 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE
                    if self.config_id.is_global_discount_tax_exclusive:
                        if not line.is_reward_line and not line.product_id.is_discount_product and line.order_id.amount_total != 0:
                            line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1 - (line.discount or 0.0) / 100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                            #taxes = taxes.compute_all(price, order_line.order_id.pricelist_id.currency_id, order_line.qty, product=order_line.product_id, partner=order_line.order_id.partner_id or False)['taxes']
                            if line.tax_ids.amount_type == 'fixed':
                                pass
                            else:
                                for custom_tax in line_taxes['taxes']:
                                    custom_tax['amount'] = (custom_tax['base'] - (custom_tax['base'] * line.global_discount_percentage/100)) * line.tax_ids_after_fiscal_position.amount/100
                        else:
                            line_taxes = {'taxes': [{'amount': 0}]}
                    else:
                        line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1 - (line.discount or 0.0) / 100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    #

                    for tax in line_taxes['taxes']:
                        taxes_amount += tax.get('amount', 0)
                        
                if line.discount > 0:
                    first_discount_amount += -(((line.price_unit * line.qty) * line.discount) / 100)
                if line.product_id.is_discount_product == True and line.price_unit < 0:
                    second_discount_amount += line.price_subtotal_incl
                discount_amount = first_discount_amount + second_discount_amount
                if line.product_id.is_discount_product == False:
                    if line.qty > 0 or line.qty < 0:

                        # 4 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE
                        if self.config_id.is_global_discount_tax_exclusive:
                            total_sale_amount += line.price_subtotal
                        else:
                            total_sale_amount += line.price_unit * line.qty
                        #
        
        # 5 KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE
        if self.config_id.is_global_discount_tax_exclusive:
            total_sale_amount = total_sale_amount + taxes_amount
        #

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
            'net_total':total_net_amount,
            'rounding':total_rounding_amount,
            'refund':total_refund_amount,
            'refund_qty' : total_refund_qty,
            'average_bill':average_bill,
            'average_pax':average_pax,
        }