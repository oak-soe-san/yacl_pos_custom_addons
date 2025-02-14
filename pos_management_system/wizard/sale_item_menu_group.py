from odoo import _, api, fields, models


class SaleItemMenuGroup(models.TransientModel):
    _name = 'sale.item.menu.group.report.wizard'
    _description = 'Sale Item Menu Group Wizard'

    date_from = fields.Datetime(string='Start From', required=False)
    date_to = fields.Datetime(string='End To', required=False)

    def action_print_excel_report(self):
        print("Excel Report")
        data = {}
        return self.env.ref('pos_management_system.sale_item_menu_group_excel_report_action').report_action(self, data=data)

    def action_print_report(self):
        start_date = self.date_from
        end_date = self.date_to

        _domain = [('date_order', '>=', start_date),
                   ('date_order', '<=', end_date)]
        pos_order_records = self.env['pos.order'].search(_domain)

        data = {}
        data['order_data'] = self._get_pos_order_data(pos_order_records)
        data['date_from'] = start_date
        data['date_to'] = end_date

        return self.env.ref('pos_management_system.sale_item_menu_group_report_action').with_context(landscape=True).report_action(self, data=data)

    def _get_pos_order_data(self, pos_order_records):
        sold_product = {}
        for order_record in pos_order_records:
            for line in order_record.lines:
                if line.product_id.pos_categ_id and line.product_id.pos_categ_id.name and line.product_id.is_discount_product == False:
                    if line.product_id.pos_categ_id.name in sold_product:
                        if line.product_id.name in sold_product[line.product_id.pos_categ_id.name]:
                            sold_product[line.product_id.pos_categ_id.name][line.product_id.name]['code'] = line.product_id.default_code
                            sold_product[line.product_id.pos_categ_id.name][line.product_id.name]['unit_price'] = line.price_unit
                            sold_product[line.product_id.pos_categ_id.name][line.product_id.name]['qty'] += line.qty
                            sold_product[line.product_id.pos_categ_id.name][line.product_id.name]['gross_sale'] += line.price_subtotal_incl
                            sold_product[line.product_id.pos_categ_id.name][line.product_id.name]['net_sale'] += line.price_subtotal
                            sold_product[line.product_id.pos_categ_id.name][line.product_id.name]['cos'] = line.product_id.standard_price
                            sold_product[line.product_id.pos_categ_id.name][line.product_id.name][
                                'profit'] += line.price_subtotal_incl - line.product_id.standard_price
                            if line.discount > 0:
                                sold_product[line.product_id.pos_categ_id.name][line.product_id.name]['discount_percentage'] += line.discount
                                sold_product[line.product_id.pos_categ_id.name][line.product_id.name][
                                    'discount_amt'] += line.price_unit - line.price_subtotal_incl
                        else:
                            sold_product[line.product_id.pos_categ_id.name].update(
                                {line.product_id.name: {
                                    'discount_amt': (line.price_unit - line.price_subtotal_incl) if line.discount > 0 else 0.00,
                                    'discount_percentage': line.discount,
                                    'code': line.product_id.default_code,
                                    'unit_price': line.price_unit,
                                    'qty': line.qty,
                                    'gross_sale': line.price_subtotal_incl,
                                    'net_sale': line.price_subtotal,
                                    'cos': line.product_id.standard_price,
                                    'profit': (line.price_subtotal_incl - line.product_id.standard_price), }})
                    else:
                        sold_product.update({
                            line.product_id.pos_categ_id.name: {
                                line.product_id.name: {
                                    'discount_amt': (line.price_unit - line.price_subtotal_incl) if line.discount > 0 else 0.00,
                                    'discount_percentage': line.discount,
                                    'code': line.product_id.default_code,
                                    'unit_price': line.price_unit,
                                    'qty': line.qty,
                                    'gross_sale': line.price_subtotal_incl,
                                    'net_sale': line.price_subtotal,
                                    'cos': line.product_id.standard_price,
                                    'profit': (line.price_subtotal_incl - line.product_id.standard_price), }}})

                # Global Discount
                elif line.product_id and line.product_id.name and line.product_id.is_discount_product == True and line.product_id.is_discount_label == False:
                    if line.full_product_name in sold_product:
                        if line.full_product_name in sold_product[line.full_product_name]:
                            sold_product[line.full_product_name][line.full_product_name]['code'] = line.product_id.default_code
                            sold_product[line.full_product_name][line.full_product_name]['unit_price'] = 0.0
                            sold_product[line.full_product_name][line.full_product_name]['qty'] += line.qty
                            sold_product[line.full_product_name][line.full_product_name]['gross_sale'] += 0.0
                            sold_product[line.full_product_name][line.full_product_name]['net_sale'] += line.price_subtotal
                            sold_product[line.full_product_name][line.full_product_name]['cos'] = 0.0
                            sold_product[line.full_product_name][line.full_product_name][
                                'profit'] += 0.0
                            sold_product[line.full_product_name][line.full_product_name]['discount_percentage'] += 0.0
                            sold_product[line.full_product_name][line.full_product_name][
                                'discount_amt'] += line.price_subtotal_incl
                        else:
                            sold_product[line.full_product_name].update(
                                {line.full_product_name: {
                                    'discount_amt': line.price_subtotal_incl,
                                    'discount_percentage': 0.0,
                                    'code': line.product_id.default_code,
                                    'unit_price': 0.0,
                                    'qty': line.qty,
                                    'gross_sale': 0.0,
                                    'net_sale': line.price_subtotal,
                                    'cos': 0.0,
                                    'profit': 0.0, }})
                    else:
                        sold_product.update({
                            line.full_product_name: {
                                line.full_product_name: {
                                    'discount_amt': line.price_subtotal_incl,
                                    'discount_percentage': 0.0,
                                    'code': line.product_id.default_code,
                                    'unit_price': 0.0,
                                    'qty': line.qty,
                                    'gross_sale': 0.0,
                                    'net_sale': line.price_subtotal,
                                    'cos': 0.0,
                                    'profit': 0.0, }}})

        sold_product = dict(sorted(sold_product.items(),
                            key=lambda item: (item[0][0].isdigit(), item[0])))
        data = {
            'datas': sold_product,
        }
        return data

    # Backup Code
    # def action_print_report(self):
    #     start_date = self.date_from
    #     end_date = self.date_to

    #     _domain = [('create_date', '>=', start_date),
    #                ('create_date', '<=', end_date)]
    #     pos_order_records = self.env['pos.order.line'].search(_domain)

    #     data = {}
    #     data['order_data'] = self._get_pos_order_data(pos_order_records)
    #     data['date_from'] = start_date
    #     data['date_to'] = end_date

    #     return self.env.ref('pos_management_system.sale_item_menu_group_report_action').with_context(landscape=True).report_action(self, data=data)

    # def _get_pos_order_data(self, pos_order_records):
    #     pos_order_record = [
    #         self._get_pos_order_info(pos_order_records),
    #     ]
    #     return pos_order_record

    # def _get_pos_order_info(self, pos_order_records):
    #     pos_product_categories = pos_order_records.mapped(
    #         'product_id.pos_categ_id')

    #     data_list = []
    #     grand_total_item_count = 0.0
    #     grand_total_gross_sale = 0.0
    #     grand_total_net_sale = 0.0

    #     for pos_product_category in pos_product_categories:
    #         pos_order_lines = pos_order_records.filtered(
    #             lambda x: x.product_id.pos_categ_id == pos_product_category)
    #         line_vals = []
    #         sub_total_item_count = 0.0
    #         sub_total_gross_sale = 0.0
    #         sub_total_item_discount = 0.0
    #         sub_total_net_sale = 0.0
    #         sub_total_cog = 0.0
    #         sub_total_profit = 0.0

    #         for pos_order_line in pos_order_lines.product_id:
    #             pos_order = pos_order_lines.filtered(
    #                 lambda x: x.product_id == pos_order_line)

    #             total_item_per_qty = 0.0
    #             total_item_gross_sale = 0.0
    #             total_item_profit = 0.0
    #             total_net_sale = 0.0
    #             total_cost_of_good = 0.0
    #             total_item_discount_amount = 0.0
    #             for order in pos_order:
    #                 total_item_per_qty += order.qty
    #                 total_net_sale += order.price_subtotal
    #                 total_cost_of_good += total_item_per_qty * pos_order_line.standard_price
    #                 total_item_discount_amount += (order.discount /
    #                                                100) * order.price_unit

    #             total_item_gross_sale += total_item_per_qty * pos_order_line.list_price
    #             total_item_profit += total_item_gross_sale - pos_order_line.standard_price

    #             val = {
    #                 'item_code': pos_order_line.default_code,
    #                 'item': str(pos_order_line.name) + "   " + 'Combo' if pos_order_line.is_pack else pos_order_line.name,
    #                 'item_unit_price': pos_order_line.list_price,
    #                 'qty': total_item_per_qty,
    #                 'total_item_gross_sale': total_item_gross_sale,
    #                 'total_item_discount_amount': total_item_discount_amount,
    #                 'total_net_sale': total_net_sale,
    #                 'cost_of_good': total_cost_of_good,
    #                 'profit': total_item_profit,
    #             }

    #             line_vals.append(val)
    #             sub_total_item_count += val['qty']
    #             sub_total_gross_sale += val['total_item_gross_sale']
    #             sub_total_item_discount += val['total_item_discount_amount']
    #             sub_total_net_sale += val['total_net_sale']
    #             sub_total_cog += val['cost_of_good']
    #             sub_total_profit += val['profit']

    #         data_list.append({
    #             'category_name': pos_product_category.name,
    #             'lines': line_vals,
    #             'sub_total_item_count': sub_total_item_count,
    #             'sub_total_gross_sale': sub_total_gross_sale,
    #             'sub_total_item_discount': sub_total_item_discount,
    #             'sub_total_net_sale': sub_total_net_sale,
    #             'sub_total_cog': sub_total_cog,
    #             'sub_total_profit': sub_total_profit,
    #         })
    #         grand_total_item_count += sub_total_item_count
    #         grand_total_gross_sale += sub_total_gross_sale
    #         grand_total_net_sale += sub_total_net_sale

    #     data = {
    #         'datas': data_list,
    #         'grand_total_item_count': grand_total_item_count,
    #         'grand_total_gross_sale': grand_total_gross_sale,
    #         'grand_total_net_sale': grand_total_net_sale,
    #     }
    #     return data
