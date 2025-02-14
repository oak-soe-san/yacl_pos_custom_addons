odoo.define('km_pos_currency.NewMultiCurrencyPopup', function (require) {
    'use strict';

    const MultiCurrencyPopup = require('sync_pos_currency.MultiCurrencyPopup');
    const Registries = require('point_of_sale.Registries');

    const NewMultiCurrencyPopup = MultiCurrencyPopup => 
        class extends MultiCurrencyPopup {
            setup() {
                super.setup();
                this.selected_value = this.values[0];
            }

            getPayload() {
                const originalPayload = super.getPayload();
                const customPayload = {
                    ...originalPayload,
                    'amount_total_currency': this.amount_total_currency,
                    'selected_value': this.selected_value
                }
                return customPayload;
            }
        }

    Registries.Component.extend(MultiCurrencyPopup, NewMultiCurrencyPopup);

    return MultiCurrencyPopup;
});