odoo.define('km_pos_global_discount_tax_exclusive.OrderlineDetailsExtend', function(require){
    'use strict';

    const OrderlineDetails = require('point_of_sale.OrderlineDetails');
    const Registries = require('point_of_sale.Registries');

    const OrderlineDetailsExtend = (OrderlineDetails) => class extends OrderlineDetails {

        get totalPrice() {
            if(this.props.line.pos.config.is_global_discount_tax_exclusive) {
                if (this.props.line.get_is_discount_product() || this.props.line.is_reward_line) {
                    return this.env.pos.format_currency(this.props.line.get_price_without_tax());
                } else {
                    return this.env.pos.format_currency(this.line.totalPrice);
                }
            } else {
                return this.env.pos.format_currency(this.line.totalPrice);
            }
        }
     
        get pricePerUnit() {
            if(this.props.line.pos.config.is_global_discount_tax_exclusive) {
                if (this.props.line.get_is_discount_product() || this.props.line.is_reward_line) {
                    return ` ${this.unit} at ${this.props.line.get_price_without_tax()} / ${this.unit}`;
                } else {
                    return ` ${this.unit} at ${this.unitPrice} / ${this.unit}`;
                }
            } else {
                return ` ${this.unit} at ${this.unitPrice} / ${this.unit}`;
            }
        }
        
    };

    Registries.Component.extend(OrderlineDetails, OrderlineDetailsExtend);
    return OrderlineDetails;
});