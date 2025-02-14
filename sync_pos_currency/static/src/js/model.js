odoo.define('sync_pos_currency.models', function (require) {
    "use strict";

    const { PosGlobalState,Payment } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;


    const PosComboProductPosGlobalState = (PosGlobalState) => class PosComboProductPosGlobalState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);

            const multi_curr = this.config.payment_currency_ids
            this.multicurrencypayment = await this.env.services.rpc({
                model: 'res.currency',
                method: 'search_read',
                fields: ['name', 'symbol', 'position', 'rounding', 'rate', 'decimal_places'],
                domain: [['id', 'in', multi_curr]],
            });


        }
    }
    Registries.Model.extend(PosGlobalState, PosComboProductPosGlobalState);

    const PosMultiCurrencyPayment = (Payment) => class PosMultiCurrencyPayment extends Payment {
        constructor(obj, options) {
            super(...arguments);
            this.selected_currency = this.selected_currency || false;
            this.selected_currency_rate = this.selected_currency_rate || 0.0
            this.selected_currency_symbol = this.selected_currency_symbol || 0.0
            this.currency_amount_total = this.currency_amount_total || 0.0
        }
        set_selected_currency(currency){
            this.selected_currency = currency;
        }
        get_selected_currency() {
            return this.selected_currency;
        }
        set_currency_symbol(symbol){
            this.selected_currency_symbol = symbol
        }
        get_currency_symbol() {
            return this.selected_currency_symbol;
        }
        set_currency_rate(rate) {
            this.selected_currency_rate = rate
        }
        get_currency_rate() {
            return this.selected_currency_rate;
        }
        set_currency_amount_paid(total) {
            this.currency_amount_total = total
        }
        get_currency_amount_paid() {
            return this.currency_amount_total;
        }
        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.selected_currency = json.selected_currency;
            this.selected_currency_symbol = json.selected_currency_symbol;
            this.selected_currency_rate = json.selected_currency_rate;
            this.currency_amount_total = json.currency_amount_total;
        }
        export_as_JSON() {
            let json = super.export_as_JSON(...arguments);
            json.selected_currency = this.get_selected_currency();
            json.selected_currency_symbol = this.get_currency_symbol();
            json.selected_currency_rate = this.get_currency_rate() || 0.0;
            json.currency_amount_total = this.get_currency_amount_paid() || 0.0;
            return json;
        }
        export_for_printing() {
            var receipt = super.export_for_printing(...arguments);
            receipt.selected_currency = this.get_selected_currency();
            receipt.selected_currency_symbol = this.get_currency_symbol();
            receipt.selected_currency_rate = this.get_currency_rate() || 0.0;
            var rounded_rate = receipt.selected_currency_rate;
            receipt.rounded_currency_rate = rounded_rate;
            receipt.currency_amount_total = this.get_currency_amount_paid() || 0.0;
            debugger;
            return receipt;
        }
    }
    Registries.Model.extend(Payment, PosMultiCurrencyPayment);
});
