odoo.define('km_pos_slip_kitchen_bar.KitchenOrderReceipt', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    const { onWillUpdateProps } = owl;

    class KitchenOrderReceipt extends PosComponent {
        setup() {
            super.setup();
            this._receiptEnv = this.props.order.getOrderReceiptEnv();

            onWillUpdateProps((nextProps) => {
                this._receiptEnv = nextProps.order.getOrderReceiptEnv();
            });
        }
        get receipt() {
            var category_ids = this.env.pos.get_kitchen_bar_categories('kitchen');
            var order = this.env.pos.get_order();
            var product_in_kitchen_bar_category = [];
            if (order) {
                var category_set = new Set();
                category_ids.forEach(function(category) {
                    category_set.add(category);
                });

                order.get_orderlines().forEach(function (orderline) {
                    var product = orderline.product;
                    var product_name = orderline.get_full_product_name();
                    if (orderline.is_product_in_kitchen_bar_category(category_set, product.id)) {
                        product_in_kitchen_bar_category.push(product_name);
                    }
                });
            }

            this.receiptEnv.receipt.orderlines = this.receiptEnv.receipt.orderlines.filter(function(item){
                return product_in_kitchen_bar_category.includes(item.product_name);
            });

            return this.receiptEnv.receipt;
        }
        get orderlines() {
            return this.receiptEnv.orderlines;
        }
        get paymentlines() {
            return this.receiptEnv.paymentlines;
        }
        datestringformat_1(){
            var options = {year: 'numeric', month: 'short', day: 'numeric' };
            var today  = new Date();
            return today.toLocaleDateString("en-US", options)
            
        }
        datestringformat_2(){
            var today  = new Date();
            var ampm = (this.receiptEnv.receipt.date.hour >= 12) ? "PM" : 'AM';
            return today.toLocaleDateString("en-US")+ ' , ' + this.receiptEnv.receipt.date.hour.toString().padStart(2, '0') + ':' + this.receiptEnv.receipt.date.minute.toString().padStart(2, '0') + ' ' + ampm
            
        }

        get isTaxIncluded() {
            return Math.abs(this.receipt.subtotal - this.receipt.total_with_tax) <= 0.000001;
        }
        get receiptEnv () {
          return this._receiptEnv;
        }
        isSimple(line) {
            return (
                line.discount === 0 &&
                line.is_in_unit &&
                line.quantity === 1 &&
                !(
                    line.display_discount_policy == 'without_discount' &&
                    line.price < line.price_lst
                )
            );
        }
    }
    KitchenOrderReceipt.template = 'KitchenOrderReceipt';

    Registries.Component.add(KitchenOrderReceipt);

    return KitchenOrderReceipt;
});
