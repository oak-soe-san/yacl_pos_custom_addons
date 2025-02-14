odoo.define('mscl_customer_id.model', function(require) {
'use strict';

const {Order} = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');


const CustomerIDButton = (Order) => class CustomerIDButton extends Order {

    constructor(obj, options) {
        super(obj, options);
        this.customerID = this.customerID || '';
    }

    export_as_JSON() {
        const json = super.export_as_JSON();
        json.customer_id = this.get_customer_id();
        return json;
        }

    init_from_JSON(json) {
            super.init_from_JSON(json);
            this.set_customer_id(json.customer_id);
        }

     export_for_printing() {
        var result = super.export_for_printing(...arguments);
        result.customer_id = this.get_customer_id();
        return result;
        }

    set_customer_id(id) {
        this.customerID = id;
    }

    get_customer_id() {
        return this.customerID;
    }
    }

Registries.Model.extend(Order, CustomerIDButton);
});