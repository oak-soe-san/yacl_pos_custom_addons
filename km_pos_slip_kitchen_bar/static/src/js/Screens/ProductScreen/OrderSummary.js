odoo.define('km_pos_slip_kitchen_bar.OrderSummary', function (require) {
    'use strict';

    const OrderSummary = require('point_of_sale.OrderSummary');
    const Registries = require('point_of_sale.Registries');

    const { useEffect } = owl;

    const CustomOrderSummary = OrderSummary =>
        class extends OrderSummary {
            setup() {
                super.setup();
                useEffect(
                    () => {
                        var order = this.env.pos.get_order();
                        var bar_category_ids = this.env.pos.get_kitchen_bar_categories('bar');
                        var kitchen_category_ids = this.env.pos.get_kitchen_bar_categories('kitchen');

                        if (order) {
                            var bar_category_set = new Set(bar_category_ids);
                            var kitchen_category_set = new Set(kitchen_category_ids);

                            order.get_orderlines().forEach(function (orderline) {
                                var product = orderline.product;
                                var product_name = orderline.get_full_product_name();
                                if (orderline.is_product_in_kitchen_bar_category(bar_category_set, product.id)) {
                                    order.set_bar_button(true);
                                } 

                                if (orderline.is_product_in_kitchen_bar_category(kitchen_category_set, product.id)) {
                                    order.set_kitchen_button(true);
                                }
                            });
                        }

                        if (order.is_kitchen_button()) {
                            $("#kitchen_slip_button").show();
                        } else {
                            $("#kitchen_slip_button").hide();
                        }

                        if (order.is_bar_button()) {
                            $("#bar_slip_button").show();
                        } else {
                            $("#bar_slip_button").hide();
                        }

                        if (this.props.order.get_total_with_tax() <= 0) {
                            $("#bar_slip_button").hide();
                            $("#kitchen_slip_button").hide();
                        }
                    }
                );
            }
        };

    Registries.Component.extend(OrderSummary, CustomOrderSummary);

    return OrderSummary;
});