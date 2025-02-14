odoo.define('km_pos_currency.models', function (require) {
    "use strict";

    const { Payment, Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const CustomOrderExtend = (Order) => class CustomOrderExtend extends Order{
        init_from_JSON(json) {
            super.init_from_JSON(json);
            this.final_change = '';
        }

        export_as_JSON(){
            const json = super.export_as_JSON(...arguments);
            json.final_change = this.final_change;
            return json;
        }

        export_for_printing() {
            var result = super.export_for_printing(...arguments);
            result.final_change = this.get_final_change();
            return result;
        }

        set_final_change(value, selected_value) {
            if (value > 0) {
                this.final_change = selected_value.symbol + ' ' + value.toFixed(selected_value.decimal_places);
            }
        }

        get_final_change() {
            return this.final_change;
        }
    }
    Registries.Model.extend(Order, CustomOrderExtend);
    
    const CustomPayment = (Payment) => class CustomPayment extends Payment {
        
        set_amount_for_change(value, selected_value) {
            this.order.set_final_change(value, selected_value);
        }
        
    }
    Registries.Model.extend(Payment, CustomPayment);
});
