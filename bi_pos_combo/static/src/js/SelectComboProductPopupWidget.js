odoo.define('bi_pos_combo.SelectComboProductPopupWidget', function(require){
	'use strict';

	const Popup = require('point_of_sale.ConfirmPopup');
	const Registries = require('point_of_sale.Registries');
	const PosComponent = require('point_of_sale.PosComponent');
	const { onMounted } = owl;


	class SelectComboProductPopupWidget extends Popup {

		setup() {
			super.setup();
			onMounted(() =>{
				var self = this;
				var order = self.env.pos.get_order();

				if(order){
					var orderlines = order.get_orderlines();
					this.product = self.props.product;
					this.update_line = self.props.update_line;
					this.required_products = self.props.required_products;
					this.optional_products = self.props.optional_products;
					this.combo_products = self.env.pos.pos_product_pack;

					$('.optional-product').each(function(){
						if(self.update_line){
							
		                    var selectedprod = parseInt(this.dataset.productId);
		                    var order = self.env.pos.get_order();
		                    var selected_product = order.get_selected_orderline()
		                    if(order){
		                        if (order.get_selected_orderline()) {
		                            if(order.get_selected_orderline().product.id == self.props.product.id){
		                                var selected_product = order.get_selected_orderline().combo_prod_ids
		                                var combo_products = self.env.pos.pos_product_pack;
		                                for (var i = 0; i < selected_product.length; i++){

		                                    if(selected_product[i] == selectedprod){
		                                        $(this).addClass('raghav');
		                                    }
		                                };
		                            }
		                        }
		                    }
		                }
		                
					});
				}
			});
		}
		go_back_screen() {
			this.showScreen('ProductScreen');
			this.env.posbus.trigger('close-popup', {
                popupId: this.props.id });
		}

		get req_product() {
			let req_product = [];
			$.each(this.props.required_products, function( i, prd ){
				prd['product_image_url'] = `/web/image?model=product.product&field=image_128&id=${prd.id}&write_date=${prd.write_date}&unique=1`;
				req_product.push(prd)
			});
			return req_product;
		}

		update_produc(id,qty){
			$("#"+id).each(function(){
				if(self.update_line){
					$(this).on('click',function () {
                        if($(this).hasClass('raghav')){
                        	$(this).removeClass('raghav');
                        }else{
                        	$(this).addClass('raghav');
                        }
					});
                    var selectedprod = parseInt(this.dataset.productId);
                    var order = self.env.pos.get_order();
                    var selected_product = order.get_selected_orderline()
                    if(order){
                        if (order.get_selected_orderline()) {
                            if(order.get_selected_orderline().product.id == self.props.product.id){
                                var selected_product = order.get_selected_orderline().combo_prod_ids
                                var combo_products = self.env.pos.pos_product_pack;
                                for (var i = 0; i < selected_product.length; i++){

                                    if(selected_product[i] == selectedprod){
                                        $(this).addClass('raghav');
                                    }
                                };
                            }
                        }
                    }
                }
                else{

					if(qty > 0){
						if(! $(this).hasClass('raghav') ){
	                    	$(this).addClass('raghav');
	                    }
					}else{
						if($(this).hasClass('raghav') ){
	                    	$(this).removeClass('raghav');
	                    }
					}

                }
			});
		}

		update_optional_product_by_id(id,qty){
			var self = this
			$.each(this.props.optional_products, function( i, prd ){
				if(prd.id == id){
					if(qty > prd.combo_limit ){
						alert("product limit exceeded")
					}else{
						prd['combo_qty'] = qty
						self.update_produc(id,qty)
					}
				}
			});
		}

		get optional_product(){
			let optional_product = [];
			$.each(this.props.optional_products, function( i, prd ){
				prd['product_image_url'] = `/web/image?model=product.product&field=image_128&id=${prd.id}&write_date=${prd.write_date}&unique=1`;
				optional_product.push(prd)
			});
			return optional_product;
		}

		plusQty(event) {
			var self = this;
			var current_product_id = parseInt(event.currentTarget.dataset['productId'])
		
			$(".qty-label").each(function( index ) {
				var prd_id_qty = parseInt($(this).attr('product-id'));
				var product = self.env.pos.db.get_product_by_id(prd_id_qty);
				if (current_product_id == prd_id_qty){
					let added_qty = parseInt($(this).text()) + 1
					if(added_qty <= product.combo_limit){
						$(this).text(added_qty);
					}
					self.update_optional_product_by_id(prd_id_qty,added_qty)

				}
			});
		}

		minusQty(event) {
			var self = this;
			var current_product_id = parseInt(event.currentTarget.dataset['productId'])


			$(".qty-label").each(function( index ) {

				var prd_id_qty = parseInt($(this).attr('product-id'));
				var product = self.env.pos.db.get_product_by_id(prd_id_qty);
				if (current_product_id == prd_id_qty){
					if (parseInt($(this).text()) > 0){
						$(this).text(parseInt($(this).text()) - 1);
						self.update_optional_product_by_id(prd_id_qty,parseInt($(this).text()))
					}
				}
			});
		}


		
		renderElement(ev) {
			var self = this;
			var order = self.env.pos.get_order();
			if(order){
				var orderlines = order.get_orderlines();
				var final_products = this.required_products;
				ev.stopPropagation();
				ev.preventDefault();
				var prod_id = parseInt(event.currentTarget.dataset['productId']);
				$(this).closest(".optional-product").hide();
				for (var i = 0; i < self.props.optional_products.length; i++)
				{
					if(self.props.optional_products[i]['id'] == prod_id)
					{
						self.props.optional_products.splice(i, 1);
					}
				}
			}
		}
		add_confirm(ev){
			var final_products = this.props.required_products;
			var order = this.env.pos.get_order();
			var orderlines = order.get_orderlines();
			ev.stopPropagation();
			ev.preventDefault();
			var self = this

			$('.raghav').each(function(){
				var prod_id = parseInt(this.dataset.productId);
				for (var i = 0; i < self.props.optional_products.length; i++) 
				{
					if(self.props.optional_products[i]['id'] == prod_id)
					{
						final_products.push(self.props.optional_products[i]); 
					}
				}
				
			});
			var add = [];
			var new_prod = [self.props.product.id,final_products];
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
			var selected_line = null;
			self.env.pos.db.bi_combo_product = [];
			if(self.props.update_line){
				orderlines.forEach(function (line) {
                    if(line.selected == true)
                    {
                        if(line.product.id == self.props.product.id)
                        {
                            selected_line = line;
                        }
					}
				});
                if(selected_line != null){
                	// console.log("final_prodycrs-------",final_products)
                    selected_line.set_combo_products(final_products)
                    self.env.pos.db.bi_combo_product.push(final_products)
                }
                else{
                    order.add_product(self.props.product);
                }

			}else{
				order.add_product(self.props.product,{merge:false})
			}
			self.env.posbus.trigger('close-popup', {
                popupId: self.props.id });
		}
	}
	
	SelectComboProductPopupWidget.template = 'SelectComboProductPopupWidget';
	Registries.Component.add(SelectComboProductPopupWidget);
	return SelectComboProductPopupWidget;

});
