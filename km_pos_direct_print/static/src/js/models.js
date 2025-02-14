odoo.define('km_pos_direct_print.models', function (require) {
    "use strict";

    var { Orderline } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrderLine = (Orderline) => class CustomOrderLine extends Orderline {
        set_printed(printed) {
            this.printed = printed;
        }

        is_printed() {
            return this.printed;
        }    

        set_printed_qty(printed_qty) {
            this.printed_qty = printed_qty;
//            this.printed = true;
        }

        get_printed_qty() {
            return this.printed_qty || 0;
        }   

        set_printed_total_qty(printed_total_qty) {
            this.printed_total_qty = printed_total_qty;
        }

        get_printed_total_qty() {
            return this.printed_total_qty || 0;
        }     

        clone(){
            const orderline = super.clone(...arguments);
            orderline.printed = this.printed;
            orderline.printed_qty = this.printed_qty;
            orderline.printed_total_qty = this.printed_total_qty;
            return orderline;
        }

        init_from_JSON(json){
            this.printed = json.printed;
            this.printed_qty = json.printed_qty;
            this.printed_total_qty = json.printed_total_qty;
            super.init_from_JSON(...arguments);
        }

        export_as_JSON(){
            const result = super.export_as_JSON(...arguments);
            result.printed = this.printed;
            result.printed_qty = this.printed_qty;
            result.printed_total_qty = this.printed_total_qty;
            return result;
        }

        export_for_printing(){
            const json = super.export_for_printing(...arguments);
            json.printed_qty = this.get_printed_qty();
            return json;
        }
    }

    Registries.Model.extend(Orderline, CustomOrderLine);
});
