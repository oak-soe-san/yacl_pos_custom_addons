odoo.define('pos_reports_omax.models', function (require) {
"use strict";

    var { Order } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrderReceipt = (Order) => class CustomOrderReceipt extends Order {
        export_for_printing() {
            var result = super.export_for_printing(...arguments);
            result['pos_bar_code'] = this._get_bar_code_data();
            return result;
        }
        _get_bar_code_data() {
            const ordername = this.name;
            var svgNode = BARCode(ordername);
            let bar_code_svg = new XMLSerializer().serializeToString(svgNode);
            return "data:image/svg+xml;base64,"+ window.btoa(bar_code_svg);
        }
    }
    Registries.Model.extend(Order, CustomOrderReceipt);
});
