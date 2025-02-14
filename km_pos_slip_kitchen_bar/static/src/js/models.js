odoo.define('km_pos_slip_kitchen_bar.models', function (require) {
    "use strict";

    var { Order, Orderline, PosGlobalState } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrder = (Order) => class CustomOrder extends Order {
        set_bar_button(bar_button) {
            this.bar_button = bar_button;
        }

        is_bar_button() {
            return this.bar_button || false;
        } 

        set_kitchen_button(kitchen_button) {
            this.kitchen_button = kitchen_button;
        }

        is_kitchen_button() {
            return this.kitchen_button || false;
        } 

        clone(){
            const order = super.clone(...arguments);
            order.bar_button = this.bar_button;
            order.kitchen_button = this.kitchen_button;
            return order;
        }

        init_from_JSON(json){
            this.bar_button = json.bar_button;
            this.kitchen_button = json.kitchen_button;            
            super.init_from_JSON(...arguments);
        }

        export_as_JSON(){
            const result = super.export_as_JSON(...arguments);
            result.bar_button = this.bar_button;
            result.kitchen_button = this.kitchen_button;
            return result;
        }
    }
    Registries.Model.extend(Order, CustomOrder); 

    const CustomOrderLine = (Orderline) => class CustomOrderLine extends Orderline {
        is_product_in_kitchen_bar_category(category_ids_set, product) {
            return this.pos.db.is_product_in_category(category_ids_set, product);
        }
    }
    Registries.Model.extend(Orderline, CustomOrderLine); 

    const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);
            this.kitchen_bar_slip = loadedData['kitchen.bar.slip'];
        }

        get_kitchen_bar_categories(printer_type) {
            var category_ids = [];
            this.kitchen_bar_slip.forEach(function (data) {
                if (data['printer_type'] == printer_type) {
                    category_ids.push(...data['product_categories_ids']);
                }
            });
            return category_ids;
        }
    }
    Registries.Model.extend(PosGlobalState, NewPosGlobalState);
});