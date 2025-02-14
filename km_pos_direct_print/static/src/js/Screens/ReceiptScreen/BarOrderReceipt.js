odoo.define('km_pos_direct_print.BarOrderReceiptExtend', function(require) {
    'use strict';

    const BarOrderReceipt = require('km_pos_slip_kitchen_bar.BarOrderReceipt');
    const Registries = require('point_of_sale.Registries');

    const BarOrderReceiptExtend = (BarOrderReceipt) => class extends BarOrderReceipt {

         setup() {
            super.setup();
            var category_ids = this.env.pos.get_kitchen_bar_categories('bar');
            var order = this.env.pos.get_order();
            var product_in_kitchen_bar_category = [];
            if (order) {
                var category_set = new Set(category_ids);
                order.get_orderlines().forEach(function (orderline) {
                    var product = orderline.product;
                    var product_name = orderline.get_full_product_name();
                    if (orderline.is_product_in_kitchen_bar_category(category_set, product.id)) {
                        if (orderline.is_printed()) {
                            if (orderline.get_printed_total_qty() < orderline.quantity) {
                                product_in_kitchen_bar_category.push(product_name);
                            }
                        } else {
                            product_in_kitchen_bar_category.push(product_name);
                        }

                    }
                });
            }

            this.receiptEnv.receipt.orderlines = this.receiptEnv.receipt.orderlines.filter(function(item){
                return product_in_kitchen_bar_category.includes(item.product_name);
            });
        }

        get receipt() {
            return this.receiptEnv.receipt;
        }

    }
    Registries.Component.extend(BarOrderReceipt, BarOrderReceiptExtend);
    return BarOrderReceipt;
});
