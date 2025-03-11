odoo.define('sync_pos_currency.MultiCurrencyPopup', function (require) {
"use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const core = require('web.core');
    const _t = core._t;
    var utils = require('web.utils');
    var round_pr = utils.round_precision;

    class MultiCurrencyPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.values = this.env.pos.multicurrencypayment
            this.selected_curr_name = this.values[0].name
            this.AmountTotal = this.env.pos.get_order().get_due()
            this.selected_rate = this.values[0].rate.toFixed(4)
            console.log("\n\n the selected rate", this.selected_rate, "\n\n")
            this.symbol = this.values[0].symbol
            this.amount_total_currency = (this.selected_rate * this.AmountTotal).toFixed(4)
            if(this.env.pos.config.cash_rounding){
                var cash_rounding = this.env.pos.cash_rounding[0].rounding;
                this.AmountTotal = round_pr(this.env.pos.get_order().get_due(),cash_rounding)
            }
        }

        getValues(event){
            this.selected_value = this.values.find((val) => val.id === parseFloat(event.target.value));
            this.selected_curr_name = this.selected_value.name;
            this.selected_rate = this.selected_value.rate.toFixed(6)
            debugger;
            this.symbol = this.selected_value.symbol
            this.amount_total_currency = (this.selected_rate * this.AmountTotal).toFixed(4)
            this.render();
        }
        getPayload() {
            return {
                currency_name: this.selected_curr_name,
                selected_rate : this.selected_rate,
                symbol : this.symbol,
            }
        }
    }
    MultiCurrencyPopup.template = 'MultiCurrencyPopup';
    Registries.Component.add(MultiCurrencyPopup);

    return MultiCurrencyPopup;
   
});
