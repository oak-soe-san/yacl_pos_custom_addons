odoo.define('km_pos_combo_customize.bi_pos_combo_extend', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	var { Orderline, Order } = require('point_of_sale.models');

	const BiCustomOrderExtend = (Order) => class BiCustomOrderExtend extends Order{

		set_orderline_options(orderline, options) {
			if(options.already_qty !== undefined){
	            orderline.already_qty = options.already_qty;
	        }
	        super.set_orderline_options(orderline, options);
	    }
	}

	Registries.Model.extend(Order, BiCustomOrderExtend);


	const BiCustomOrderLineExtend = (Orderline) => class BiCustomOrderLineExtend extends Orderline{

		prepare_combo_list(list_data){
			this.product.order_line_qty = 0;
			var combo_data = [];
			list_data.forEach(function (prod) {
				if(prod != null){

					var prd_data = {
						'active': prod.active,
						'applicablePricelistItems': prod.applicablePricelistItems,
						'attribute_line_ids' : prod.attribute_line_ids,
						'available_in_pos': prod.available_in_pos,
						'barcode': prod.barcode,
						'categ': prod.categ,
						'categ_id': prod.categ_id,
						'cid': prod.cid,
						'combo_qty': prod.combo_qty,
						'old_combo_qty': prod.old_combo_qty,
						'new_combo_qty': prod.new_combo_qty,
						'combo_limit': prod.combo_limit,
						'default_code': prod.default_code,
						'description': prod.description,
						'description_sale': prod.description_sale,
						'display_name': prod.display_name,
						'id': prod.id,
						'lst_price': prod.lst_price,
						'is_pack': prod.is_pack,
						'pack_ids': prod.pack_ids,
						'standard_price': prod.standard_price,
						'taxes_id': prod.taxes_id,
						'type': prod.type,
						'image_128': prod.image_128,
						'invoice_policy': prod.invoice_policy,
						'optional_product_ids': prod.optional_product_ids,
						'parent_category_ids': prod.parent_category_ids,
						'pos_categ_id': prod.pos_categ_id,
						'product_image_url': prod.product_image_url,
						'product_tmpl_id': prod.product_tmpl_id,
						'to_weight': prod.to_weight,
						'tracking': prod.tracking,
						'uom_id': prod.uom_id,
						"__last_update": prod.__last_update
					}

					combo_data.push(prd_data)
				}
			});
			return combo_data;
		}

		set_quantity(quantity, keep_price) {
			if(quantity) {
				if(quantity != 'remove' && this.already_qty_done) {
					if (this.quantity > 1) {
						alert("Combo is already set, Please Edit Item!");
						return true;
					}
				}
			}

			if (this.combo_products) {
				var combo_data = [];
				this.combo_products.forEach(function (prd_data) {
					if (prd_data.old_combo_qty) {
						// next time set_quantity click
						prd_data.new_combo_qty = quantity;
						prd_data.combo_qty = prd_data.old_combo_qty * quantity;
						combo_data.push(prd_data);
					} else {
						// first time set_quantity click
						prd_data.old_combo_qty = prd_data.combo_qty;
						prd_data.new_combo_qty = quantity;
						prd_data.combo_qty = prd_data.combo_qty * quantity;
						combo_data.push(prd_data);
					}
				});
				this.combo_products = combo_data;
			}

			return super.set_quantity(quantity, keep_price);
		}

	}

	Registries.Model.extend(Orderline, BiCustomOrderLineExtend);
});