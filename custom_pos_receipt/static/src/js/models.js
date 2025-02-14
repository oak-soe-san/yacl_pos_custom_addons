odoo.define('custom_pos_receipt.models', function (require) {
"use strict";

    var { Order } = require('point_of_sale.models');
    var { Orderline } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrder = (Order) => class CustomOrder extends Order {
        export_for_printing() {
            var result = super.export_for_printing(...arguments);
            result.fiscal_position = this.fiscal_position ? this.fiscal_position.name : '';
            result.client = this.get_partner();
            return result;
            }
        }
        Registries.Model.extend(Order, CustomOrder); 
    
    const CustomOrderLines = (Orderline) => class CustomOrderLines extends Orderline {
        export_for_printing() {
            var result = super.export_for_printing(...arguments);
            result.default_code = this.get_product().default_code;
            result.bar_code = this.get_product().barcode;
            return result;
            }
        }
        Registries.Model.extend(Orderline, CustomOrderLines); 
    });
