odoo.define('km_pos_combo_customize.NewSelectComboProductPopupWidget', function (require) {
    'use strict';

    const SelectComboProductPopupWidget = require('bi_pos_combo.SelectComboProductPopupWidget');
    const Registries = require('point_of_sale.Registries');

    const NewSelectComboProductPopupWidget = SelectComboProductPopupWidget =>
        class extends SelectComboProductPopupWidget {

        	update_optional_product_by_id(id, qty){
        		var self = this
        		$.each(this.props.optional_products, function( i, prd ){
					if(prd.id == id){
						prd['combo_qty'] = qty
						self.update_produc(id,qty)
					}
				});

				$.each(this.props.required_products, function( i, prd ){
					if(prd.id == id){
						prd['combo_qty'] = qty
						self.update_produc(id,qty)
					}
				});
			}

			plusQty(event) {
				var combo_limit = this.props.product.combo_limit;
				if(this.props.required_products.length > 0) {
					if (this.props.required_products[0].new_combo_qty) {
						combo_limit = combo_limit * this.props.required_products[0].new_combo_qty;
					}
				} else if (this.props.optional_products[0].new_combo_qty) {
					combo_limit = combo_limit * this.props.optional_products[0].new_combo_qty;
				} else if (this.product.order_line_qty > 0){
					combo_limit = combo_limit * this.product.order_line_qty;
				}

				var total_qty = 1;
				var result = true;
				$(".qty-label").each(function(index) {
					total_qty += parseInt($(this).text());
					if(total_qty > combo_limit) {
						result = false;
					}
				});

				var current_product_id = parseInt(event.currentTarget.dataset['productId']);
				var self = this;
				$(".qty-label").each(function( index ) {
					var prd_id_qty = parseInt($(this).attr('product-id'));
					var product = self.env.pos.db.get_product_by_id(prd_id_qty);					
					if (current_product_id == prd_id_qty){
						let added_qty = parseInt($(this).text()) + 1
						if (result) {
							$(this).text(added_qty);
							self.update_optional_product_by_id(prd_id_qty,added_qty)
						}
					}
				});

				if (!result) {
					alert("product limit exceeded");
				}
			}

			minusQtyRequired(event) {
				var self = this;
				var current_product_id = parseInt(event.currentTarget.dataset['productId']);

				$(".qty-label").each(function( index ) {
					var prd_id_qty = parseInt($(this).attr('product-id'));
					var product = self.env.pos.db.get_product_by_id(prd_id_qty);
					if (current_product_id == prd_id_qty){
						if (parseInt($(this).text()) > 1){
							$(this).text(parseInt($(this).text()) - 1);
							self.update_optional_product_by_id(prd_id_qty,parseInt($(this).text()));
						} else {
							alert("Please provide at least one required product");
						}
					}
				});
			}

			minusQty(event) {
				var self = this;
				var current_product_id = parseInt(event.currentTarget.dataset['productId']);

				$(".qty-label").each(function( index ) {
					var prd_id_qty = parseInt($(this).attr('product-id'));
					var product = self.env.pos.db.get_product_by_id(prd_id_qty);
					if (current_product_id == prd_id_qty){
						if (parseInt($(this).text()) > 0){
							$(this).text(parseInt($(this).text()) - 1);
							self.update_optional_product_by_id(prd_id_qty,parseInt($(this).text()));
						}
					}
				});
			}
        
        };

    Registries.Component.extend(SelectComboProductPopupWidget, NewSelectComboProductPopupWidget);

    return SelectComboProductPopupWidget;
});