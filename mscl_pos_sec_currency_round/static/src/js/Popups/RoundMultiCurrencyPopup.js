odoo.define('secondary_currency_rounding.NewMultiCurrencyPopup_test', function (require) {
    'use strict';

    const MultiCurrencyPopup = require('sync_pos_currency.MultiCurrencyPopup');
    const Registries = require('point_of_sale.Registries');

    const NewMultiCurrencyPopup_test = MultiCurrencyPopup =>
        class extends MultiCurrencyPopup {
            setup() {
                super.setup();
                this.amount_total_currency = Math.ceil(((this.selected_rate * this.AmountTotal).toFixed(4))/50)*50
            }

        }

    Registries.Component.extend(MultiCurrencyPopup, NewMultiCurrencyPopup_test);

    return MultiCurrencyPopup;
});