from odoo import models, fields, api
import json

class pos_order_line(models.Model):
	_inherit = 'pos.order.line'

	combo_product_and_qty = fields.Text("Combo Produts")
	is_combo_member = fields.Text("Combo Inside Produts", default=False)

	@api.model_create_multi
	def create(self, vals_list):
		for order_line in vals_list:
			order = self.env['pos.order'].browse(order_line['order_id'])
			use_combo = order.config_id.use_combo

		if use_combo:
			for order_line in vals_list:
				if 'combo_products' in order_line:
					combo_products_json = order_line['combo_products']
					combo_products_dict = json.loads(combo_products_json)
					result = ''
					for combo_product in combo_products_dict:
						result += combo_product['display_name'] + ' x ' + str(combo_product['combo_qty']) + ', '
						new_order_line = {'qty': 1, 'product_id': 1, 'full_product_name': '', 'order_id': 1, 'price_subtotal': 0, 'price_subtotal_incl': 0, 'is_combo_member': True}
						new_order_line['qty'] = combo_product['combo_qty']
						new_order_line['product_id'] = combo_product['id']
						new_order_line['full_product_name'] = combo_product['display_name']
						new_order_line['order_id'] = order_line['order_id']
						vals_list.append(new_order_line)
					else:
						result = result[:-2]
					order_line['combo_product_and_qty'] = result

				elif 'refunded_orderline_id' in order_line:
					pos_order_line = self.env['pos.order.line'].browse(order_line['refunded_orderline_id'])
					if pos_order_line.product_id.is_pack:
						order_line['combo_prod_ids'] = pos_order_line.combo_prod_ids
						refund_combo_products_json =  pos_order_line.combo_products
						refund_combo_products_dict = json.loads(refund_combo_products_json)
						result = ''
						for combo_product in refund_combo_products_dict:
							result += combo_product['display_name'] + ' x ' + str(combo_product['combo_qty']) + ', '
							new_order_line = {'qty': -1, 'product_id': 1, 'full_product_name': '', 'order_id': 1, 'price_subtotal': 0, 'price_subtotal_incl': 0, 'is_combo_member': True}
							new_order_line['qty'] = -combo_product['combo_qty']
							new_order_line['product_id'] = combo_product['id']
							new_order_line['full_product_name'] = combo_product['display_name']
							new_order_line['order_id'] = order_line['order_id']
							vals_list.append(new_order_line)
						else:
							result = result[:-2]
						order_line['combo_product_and_qty'] = result

		return super().create(vals_list)

	def _export_for_ui(self, orderline):
		result = super()._export_for_ui(orderline)
		if self.order_id.config_id.use_combo:
			if orderline.is_combo_member:
				return {}
		return result