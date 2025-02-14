odoo.define('sync_pos_currency.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;

    const PosMultiCurrPaymentScreen = (PaymentScreen_) =>
          class extends PaymentScreen_ {
              async payMultipleCurrency() {

                if(!_.isEmpty(this.env.pos.multicurrencypayment)){
                    var payment_method_data = []
                    _.each(this.payment_methods_from_config, function(id){
                        payment_method_data.push(id)
                    });
                    const { confirmed, payload } = await this.showPopup('MultiCurrencyPopup', {
                        'payment_method': payment_method_data
                    });
                    if (confirmed) {
                        if ($(".pay_amount").val()){
                            var payment_method = parseInt($(".payment-method-select").val())
                            var currency_amount = $(".pay_amount").val()
                            var get_amount = currency_amount / payload.selected_rate
                            if(this.env.pos.config.cash_rounding){
                                var cash_rounding = this.env.pos.cash_rounding[0].rounding;
                                get_amount = round_pr(get_amount, cash_rounding);
                            }

                            let result = this.currentOrder.add_paymentline(this.env.pos.payment_methods_by_id[payment_method]);
                            this.selectedPaymentLine.set_amount(get_amount);
                            this.selectedPaymentLine.set_selected_currency(payload.currency_name);
                            this.selectedPaymentLine.set_currency_symbol(payload.symbol);
                            this.selectedPaymentLine.set_currency_rate(payload.selected_rate);
                            this.selectedPaymentLine.set_currency_amount_paid(currency_amount);
                        }
                        else {
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Amount Not Added'),
                                body: this.env._t('Please Enter the Amount!!'),
                            });
                        }
                    }
                    else{
                        return
                    }
                }
                else{
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('Currency Not Configured'),
                        body: this.env._t('Please Configure The Currency For Multi-Currency Payment.')
                    });
                    return;
                }
              }
          }

    Registries.Component.extend(PaymentScreen, PosMultiCurrPaymentScreen);

    return PaymentScreen;
});
