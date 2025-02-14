odoo.define('km_pos_combo_customize.BiProductScreenExtend', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const ProductScreen = require('point_of_sale.ProductScreen'); 
	const { useListener } = require("@web/core/utils/hooks");

	const BiProductScreenExtend = (ProductScreen) => class extends ProductScreen {

		setup() {
            super.setup();
                useListener('click-combo-set', this._clickComboSet);
                this.is_combo_set_click = false;
            }

            async _clickComboSet(event) {
                this.is_combo_set_click = true;

                var self = this;
                const product = event.detail;
                let order = this.env.pos.get_order();

                if(product.is_pack) {
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
                    //self.showPopup('SelectComboProductPopupWidget', {'product': product,'required_products':required_products,'optional_products':optional_products , 'update_line' : false });
                    
                }

                var final_products = required_products;
                var add = [];
                var new_prod = [product.id,final_products];
                if(self.env.pos.final_products)
                {
                    add.push(self.env.pos.pos_product)
                    add.push(new_prod)
                    self.env.pos.final_products = add;
                }
                else{
                    add.push(new_prod)
                    self.env.pos.final_products = add;
                }

                order.add_product(product,{merge: false, already_qty:true});
            }

			async _clickProduct(event) {
				if (this.is_combo_set_click === true) {
                    this.is_combo_set_click = false;
                    return false;
                }
				const product = event.detail;
				product.order_line_qty = 0;
				super._clickProduct(event);
			}
		};

	Registries.Component.extend(ProductScreen, BiProductScreenExtend);
	return ProductScreen;
});