odoo.define('km_pos_direct_print.BillKitchenButtonExtend', function(require) {
    'use strict';

    const BillKitchenButton = require('km_pos_slip_kitchen_bar.BillKitchenButton');
    const Registries = require('point_of_sale.Registries');

    const BillKitchenButtonExtend = (BillKitchenButton) => class extends BillKitchenButton {
        async onClick() {
            const order = this.env.pos.get_order();

            var category_ids = this.env.pos.get_kitchen_bar_categories('kitchen');
            if (order) {
                var category_set = new Set(category_ids);
                order.get_orderlines().forEach(function (orderline) {
                    var product = orderline.product;
                    var product_name = orderline.get_full_product_name();
                    if (orderline.is_product_in_kitchen_bar_category(category_set, product.id)) {
                        if (orderline.printed_total_qty != orderline.quantity){
                           var new_quantity = orderline.quantity - orderline.get_printed_total_qty();
                        }
                        else {
                           var new_quantity = 0;
                        }
                        orderline.set_printed_qty(new_quantity)
                        orderline.set_printed_total_qty(orderline.quantity)
                    }
                });
            }
            
            if (order.get_orderlines().length > 0) {
                await this.showTempScreen('KitchenBillScreen');
            } else {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Nothing to Print'),
                    body: this.env._t('There are no order lines'),
                });
            }
        }
    }

    Registries.Component.extend(BillKitchenButton, BillKitchenButtonExtend);
    return BillKitchenButton;
});
