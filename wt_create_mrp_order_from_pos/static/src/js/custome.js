odoo.define('wt_create_mrp_order_from_pos.models_mrp_order', function (require) {
"use strict";

const PaymentScreen = require('point_of_sale.PaymentScreen');
const Registries = require('point_of_sale.Registries');

	const models_mrp_order = PaymentScreen =>
        class extends PaymentScreen {
        	async validateOrder(isForceValidate) {
                await super.validateOrder(isForceValidate);
            }
        };

    Registries.Component.extend(PaymentScreen, models_mrp_order);
    return PaymentScreen;
});
