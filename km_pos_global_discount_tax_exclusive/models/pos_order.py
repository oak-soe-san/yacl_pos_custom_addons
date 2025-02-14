from odoo import fields, models, api

class PosOrder(models.Model):
	_inherit = 'pos.order'

	rounding_error = fields.Float()
	rounding_error_fix = fields.Boolean(default=False)

	@api.model_create_multi
	def create(self, vals_list):
		order = super().create(vals_list)
		if order.config_id.is_global_discount_tax_exclusive:
			debit_cash = 0 
			debit_global_discount = 0 
			credit_product_total = 0 
			credit_tax = 0
			rounding_error = 0

			debit_cash = abs(order.amount_total)
			currency = self.env.company.currency_id

			for order_line in order.lines:
				is_discount_or_reward = False
				if order_line.product_id.is_discount_product or order_line.is_reward_line:
					is_discount_or_reward = True
					tax_ids = self.env['account.tax'].search([('name', '=', 'Tax For Global Discount')])
					debit_global_discount = abs(order_line['price_subtotal'])

				check_refund = lambda x: x.qty * x.price_unit < 0
				is_refund = check_refund(order_line)

				tax_ids = order_line.tax_ids_after_fiscal_position.filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
				tax_data = tax_ids.compute_all(price_unit=order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0), quantity=abs(order_line.qty), currency=currency, is_refund=is_refund)
				taxes = tax_data['taxes']

				if not is_discount_or_reward:
					credit_product_total += abs(order_line.price_subtotal)

					if order_line.global_discount_percentage > 0:
						for custom_tax in taxes:
							if custom_tax['amount'] < 0:
								custom_tax['amount'] = currency.round(-((abs(custom_tax['base']) - (abs(custom_tax['base']) * order_line.global_discount_percentage/100)) * tax_ids.amount/100))
							else:
								custom_tax['amount'] = currency.round((abs(custom_tax['base']) - (abs(custom_tax['base']) * order_line.global_discount_percentage/100)) * tax_ids.amount/100)

							credit_tax += abs(custom_tax['amount'])
			credit = 0
			credit = currency.round(credit_product_total + credit_tax)
			debit = 0
			debit = currency.round(debit_cash + debit_global_discount)
			if credit == debit:
				pass
			else:
				rounding_error = credit - debit
			order.write({'rounding_error': rounding_error})

		return order

class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'

	global_discount_percentage = fields.Integer('Global Discount %')
	for_refund_price = fields.Float()

	@api.model_create_multi
	def create(self, vals_list):
		for order_line in vals_list:
			order = self.env['pos.order'].browse(order_line['order_id'])
			is_global_discount_tax_exclusive = order.config_id.is_global_discount_tax_exclusive

		if is_global_discount_tax_exclusive:
			global_discount_percentage = 0

			for order_line in vals_list:
				full_product_name = order_line['full_product_name']
				product = self.env['product.product'].browse(order_line['product_id'])
				if not product.is_ewallet_product:
					if product.is_discount_product and '(' in full_product_name:
						global_discount_percentage = int(full_product_name[full_product_name.rfind('(')+1:full_product_name.rfind('%)')])
					
					if 'is_reward_line' in order_line and order_line['is_reward_line']:
						reward = self.env['loyalty.reward'].browse(order_line['reward_id'])
						global_discount_percentage = reward.discount

				if 'refunded_orderline_id' in order_line:
					pos_order_line = self.env['pos.order.line'].browse(order_line['refunded_orderline_id'])
					if pos_order_line.for_refund_price != 0:
						global_discount_percentage = pos_order_line.global_discount_percentage

			for order_line in vals_list:
				product = self.env['product.product'].browse(order_line['product_id'])
				order_line['global_discount_percentage'] = global_discount_percentage

				if product.is_ewallet_product:
					pass

				elif 'is_reward_line' in order_line:
					if order_line['is_reward_line']:
						order_line['for_refund_price'] = order_line['price_unit']
						order_line['price_unit'] = order_line['price_subtotal']
						order_line['price_subtotal_incl'] = order_line['price_subtotal']

						if 'refunded_orderline_id' in order_line:
							order_line['price_unit'] = -order_line['price_unit']
							order_line['for_refund_price'] = -order_line['for_refund_price']

				elif order.config_id.module_pos_discount and order.config_id.discount_product_id:
					if product.is_discount_product:
						order_line['for_refund_price'] = order_line['price_unit']
						order_line['price_unit'] = order_line['price_subtotal']
						order_line['price_subtotal_incl'] = order_line['price_subtotal']

						if 'refunded_orderline_id' in order_line:
							order_line['price_unit'] = -order_line['price_unit']
							order_line['for_refund_price'] = -order_line['for_refund_price']
		return super().create(vals_list)

	def _export_for_ui(self, orderline):
		result = super()._export_for_ui(orderline)
		if self.order_id.config_id.is_global_discount_tax_exclusive:
			for_refund_price = orderline.for_refund_price
			if for_refund_price != 0:
				result['price_unit'] = for_refund_price
				result['price_subtotal'] = for_refund_price
				result['price_subtotal_incl'] = for_refund_price
		return result