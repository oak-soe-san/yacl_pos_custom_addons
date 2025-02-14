odoo.define('am_pos_order_ref.models', function (require) {
    "use strict";

    var { Order, PosGlobalState } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');
    const PaymentScreen = require('point_of_sale.PaymentScreen');

    const CustomOrder = (Order) => class CustomOrder extends Order {
        
        constructor(obj, options) {
            super(obj, options);
            var self = this;

            self.pos_order_ref = false;
            self.ignore = false;
            self.pos_orders_count = 0;
            self.ignore = this.compute_order_ignore();

            if(options.json) {
                self.pos_order_ref = options.json.pos_order_ref || self.compute_order_ref();
                self.pos_orders_count = options.json.pos_orders_count || 0;
            }
        }

        init_from_JSON(json) {
            super.init_from_JSON(json);

            this.pos_order_ref = json.pos_order_ref || this.compute_order_ref();
            this.pos_orders_count = json.pos_orders_count || 0;
            this.ignore = this.compute_order_ignore();
        }

        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            var orders = this.pos.db.get_unpaid_orders();
            var pending_orders = orders.filter(o => o.lines.length > 0);

            if (this.pos_order_ref) {
                json.pos_order_ref = this.pos_order_ref;
            } else {
                 if(pending_orders.length > 0) {
                    var orderRef = json.pos_order_ref || this.compute_order_ref();
                    json.pos_order_ref = orderRef;
                    this.pos_order_ref = orderRef;
                } else {
                    json.pos_order_ref = false;
                }
            }

            json.ignore = this.compute_order_ignore();
            json.pos_orders_count = pending_orders.filter(o => o.ignore == false).length;
            // console.log("pendingOrders", pending_orders.map(p => [p.pos_order_ref, p.ignore]));
            // console.log("json", json);
            return json;
        }

        compute_order_ignore() {
            var self = this;
            var seq = self.pos.config.sequence;
            var new_number = parseInt(seq.number_next_actual);
            var order_ref = self.pos_order_ref || self.compute_order_ref();

            if (order_ref) {
                var order_number = parseInt(order_ref.replace(/[^0-9]/gi, ''));
                return order_number < new_number;
            } else {
                return false;
            }
        }

        compute_order_ref() {
            var self = this;
            var unpaid_orders = self.pos.db.get_unpaid_orders();
            var seq = self.pos.config.sequence;

            var pending_orders = unpaid_orders.filter(o => o.ignore == false && o.lines.length > 0);
            var order_index = pending_orders.findIndex(o => o.name == self.name);
            var old_order_ref = pending_orders.filter(o => o.name == self.name);

            if (order_index < 0) { return false; }

            if (old_order_ref.length > 0 && old_order_ref[0].amount_total > 0 && old_order_ref[0].pos_order_ref) {
                return old_order_ref[0].pos_order_ref;
            } else {

                var new_number = parseInt(seq.number_next_actual) + (order_index > 0 ? order_index : 0);
                const zeroPad = (num, places) => String(num).padStart(places, '0');

                return seq.prefix + zeroPad(new_number, 4);
            }
        }

        export_for_printing() {
            var result = super.export_for_printing(...arguments);
            result.pos_order_ref = this.pos_order_ref;
            return result;
        }
    }

    Registries.Model.extend(Order, CustomOrder);

    const CustomPosGlobalState = (PosGlobalState) => class CustomPosGlobalState extends PosGlobalState {

        //@override
        async _processData(loadedData) {
            await super._processData(...arguments);
        
            this.ir_sequence = loadedData['ir.sequence'];
            this.config.sequence = this.ir_sequence[0];
        }

        update_order_ref() {
                var self = this;
                rpc.query({
                    'method': 'update_order_ref',
                    'model': 'pos.order',
                    'args':[self.config.sequence_id[0]]
                }).then(function (data) {
                  var seq = self.config.sequence;
                  seq.number_next_actual = data;
                }).catch(function (error){
                    var seq = self.config.sequence;
                    seq.number_next_actual += 1;
            });
        }
    }

    Registries.Model.extend(PosGlobalState, CustomPosGlobalState);

    const PaymentScreenWidget = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
            }

        async validateOrder(isForceValidate) {
            const res = await super.validateOrder(...arguments);
            var self = this;

            self.env.pos.update_order_ref();
        }
    };

    Registries.Component.extend(PaymentScreen, PaymentScreenWidget);

});