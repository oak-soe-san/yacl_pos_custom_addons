odoo.define('km_pos_combo_customize.OrderWidgetExtend', function(require){
	'use strict';

	const OrderWidget = require('point_of_sale.Orderline');
	const Registries = require('point_of_sale.Registries');
	const { Component } = owl;

	const OrderWidgetExtend = (OrderWidget) => class extends OrderWidget {
			
    	on_click(){
    		this.props.line.product.order_line_qty = this.props.line.quantity;

    		if(this.props.line['already_qty_done'] == undefined) {
    			this.props.line.already_qty_done = false;
    		}

    		if (this.props.line.already_qty) {
    			if (this.props.line.quantity == 1) {
    				alert("Please Provide Combo Qty!");
					return true;
				} else {
					if (this.props.line.quantity > 1) {
						this.props.line.already_qty_done = true;
					}
				}
			}
		    else {
		    	if (this.props.line.quantity > 1) {
					alert("Combo is already set, Please Change Combo Qty!");
					return true;
				}
    		}

    		super.on_click();
    	}
	};

	Registries.Component.extend(OrderWidget, OrderWidgetExtend);
	return OrderWidget;
});