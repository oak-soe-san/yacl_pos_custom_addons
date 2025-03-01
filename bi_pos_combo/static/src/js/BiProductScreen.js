
// BiProductScreen js
odoo.define('bi_pos_combo.BiProductScreen', function(require) {
	"use strict";

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require("@web/core/utils/hooks");
	const ProductScreen = require('point_of_sale.ProductScreen'); 
	const NumberBuffer = require('point_of_sale.NumberBuffer');

	const BiProductScreen = (ProductScreen) =>
		class extends ProductScreen {
			setup() {
				super.setup();

			}
			async _clickProduct(event) {
				var self = this;
				const product = event.detail;
				let order = this.env.pos.get_order();
				if(product.to_weight && this.env.pos.config.iface_electronic_scale){
					this.gui.show_screen('scale',{product: product});
				}else{
					if(product.is_pack)
					{
						var required_products = [];
						var optional_products = [];
						var combo_products = self.env.pos.product_pack;
						if(product)
						{
							for (var i = 0; i < combo_products.length; i++) {
								if(combo_products[i]['bi_product_product'][0] == product['id'])
								{
									if(combo_products[i]['is_required'])
									{
										combo_products[i]['product_ids'].forEach(function (prod) {
											var sub_product = self.env.pos.db.get_product_by_id(prod);
											sub_product['combo_qty'] = 1
											required_products.push(sub_product)
										});
									}
									else{
										combo_products[i]['product_ids'].forEach(function (prod) {
											var sub_product = self.env.pos.db.get_product_by_id(prod);
											sub_product['combo_qty'] = 0

											optional_products.push(sub_product)
										});
									}
								}
							}
						}
						self.showPopup('SelectComboProductPopupWidget', {'product': product,'required_products':required_products,'optional_products':optional_products , 'update_line' : false });
	                	
					}
					else{
						if (!this.currentOrder) {
		                this.env.pos.add_new_order();
			            }
			            const product = event.detail;
			            const options = await this._getAddProductOptions(product);
			            // Do not add product if options is undefined.
			            if (!options) return;
			            // Add the product after having the extra information.
			            await this._addProduct(product, options);
			            NumberBuffer.reset();
					}
				}
			}

			_setValue(val){
				let self = this;
				let order = this.currentOrder;
				if(this.currentOrder.get_selected_orderline()){
					if(this.currentOrder.get_selected_orderline().product.is_pack){
						if(this.state.numpadMode==='quantity'){
							var orderline = order.get_selected_orderline()
	                    	orderline.set_quantity(val,'keep_price')

						}else{
							super._setValue(val);
						}
					}	
					else{
						super._setValue(val);
					}
				}
				
			}
		};

	Registries.Component.extend(ProductScreen, BiProductScreen);

	return ProductScreen;

});
