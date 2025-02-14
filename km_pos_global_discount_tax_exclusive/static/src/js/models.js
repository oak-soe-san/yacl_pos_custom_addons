odoo.define('km_pos_global_discount_tax_exclusive.models', function (require) {
	"use strict";

	var { Orderline, Order } = require('point_of_sale.models');
	var Registries = require('point_of_sale.Registries');
	var { Gui } = require('point_of_sale.Gui');
	var core = require('web.core');
	var _t = core._t;

	var utils = require('web.utils');
	var round_pr = utils.round_precision;

	const CustomOrder = (Order) => class CustomOrder extends Order {

		// override 
		get_total_discount() {
	        if(this.pos.config.is_global_discount_tax_exclusive) {
	        	const ignored_product_ids = this._get_ignored_product_ids_total_discount()
		        return round_pr(this.orderlines.reduce((sum, orderLine) => {
		            if (!ignored_product_ids.includes(orderLine.product.id)) {
		                //sum += (orderLine.get_unit_price() * (orderLine.get_discount()/100) * orderLine.get_quantity());
		                if (orderLine.get_taxes().length > 0) {
		                	sum += ((orderLine.get_unit_price() / (1 + (orderLine.get_taxes()[0].amount/100))) * (orderLine.get_discount()/100) * orderLine.get_quantity());
		                } 
		                if (orderLine.display_discount_policy() === 'without_discount'){
		                    sum += ((orderLine.get_lst_price() - orderLine.get_unit_price()) * orderLine.get_quantity());
		                }
		            }
		            return sum;
		        }, 0), this.pos.currency.rounding);
	        } else {
	        	var result = super.get_total_discount();
	        	return result;
	        }
	    }
	}

	Registries.Model.extend(Order, CustomOrder);

	const CustomOrderLine = (Orderline) => class CustomOrderLine extends Orderline {

		get_is_discount_product(){
        	return this.product.is_discount_product;
    	}

    	get_is_ewallet_product(){
        	return this.product.is_ewallet_product;
    	}

		get_full_product_name () {
	        var full_name = super.get_full_product_name();
	        if (full_name.includes(', Tax:')) {
        		full_name = full_name.replace(full_name.substring(full_name.indexOf(','), full_name.indexOf(')')),'')
        	}
	        return full_name;
    	}

		// override
		get_unit_display_price(){
			if(this.pos.config.is_global_discount_tax_exclusive) {

				if(this.pos.config.module_pos_discount && this.pos.config.discount_product_id) {

					var discount_product_id = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);
					if (discount_product_id == undefined) {
						Gui.showPopup('ErrorTracebackPopup', {
	                        title: _t('Global Discount Product Must Be Available in POS'),
	                        body: _t('Go to Product Menu > Find Global Discount Product and Tick > Available in POS !'),
	                        exitButtonIsShown: true
	                    });
	                    return false;
					} else if(!discount_product_id.is_discount_product) {
						var product_name = discount_product_id.display_name;
			    		Gui.showPopup('ErrorTracebackPopup', {
	                        title: _t('Global Discount Product (' + product_name  + ') Must Be Is Discount Product'),
	                        body: _t('Go to Product Menu > Find Global Discount Product (' + product_name  + ') and Tick > Is Discount Product !'),
	                        exitButtonIsShown: true
	                    });
	                    return false;
	                }
		    	}

		    	const order = this.pos.get_order();
	    		for (const line of order._get_reward_lines()) {
	    			var product_id = line.get_product();
	                if (!product_id.is_discount_product) {
	                	var product_name = product_id.display_name;
	                	Gui.showPopup('ErrorTracebackPopup', {
	                        title: _t('Reward Product (' + product_name  + ') Must Be Is Discount Product'),
	                        body: _t('Go to Product Menu > Find Reward Product (' + product_name  + ') and Tick > Is Discount Product !'),
	                        exitButtonIsShown: true
	                    });
	                    return false;
	                }
	            }

		    	var global_discount_tax = true;
		    	this.pos.taxes.forEach((tax) => {
		    		if (tax.name == 'Tax For Global Discount') {
		    			global_discount_tax = false;
		    		}
		    	});

		    	if (global_discount_tax) {
		    		Gui.showPopup('ErrorTracebackPopup', {
                        title: _t('Global Discount Tax Not Found'),
                        body: _t('Go to Accounting or Invoicing Menu > Configuration > Taxes > Create - Name Tax For Global Discount and Amount 0% !'),
                        exitButtonIsShown: true
                    });
                    return false;
	    		}

    			if(this.get_is_discount_product()) {
            		return this.get_price_without_tax();
	            }

				if(this.is_reward_line !== undefined) {
					if (this.is_reward_line) {
						return this.get_price_without_tax();
					}
		        }

			    if (this.pos.config.iface_tax_included === 'total') {
		            return this.get_all_prices(1).priceWithTax;
		        } else {
		            return this.get_unit_price();
		        }
	    	} else {
	    		var result = super.get_unit_display_price();
	        	return result;
	    	}
    	}

        // override
		get_display_price(){
			if(this.pos.config.is_global_discount_tax_exclusive) {
				
				if (!this.get_is_ewallet_product()) {
					if(this.get_is_discount_product()) {
		            	return this.get_price_without_tax();
			        }

			        if(this.is_reward_line !== undefined) {
						if(this.is_reward_line) {
				            return this.get_price_without_tax();
				        }
				    }
				}
			    
			    if (this.pos.config.iface_tax_included === 'total') {
		            return this.get_price_with_tax();
		        } else {
		            return this.get_base_price();
		        }
			} else {
				var result = super.get_display_price();
	        	return result;
			}
        }
	}

	Registries.Model.extend(Orderline, CustomOrderLine);
});