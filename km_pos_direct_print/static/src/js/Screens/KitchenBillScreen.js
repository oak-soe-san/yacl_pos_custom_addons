odoo.define('km_pos_direct_print.KitchenBillScreenExtend', function (require) {
    'use strict';

    const KitchenBillScreen = require('km_pos_slip_kitchen_bar.KitchenBillScreen');
    const Registries = require('point_of_sale.Registries');
    const { Printer } = require('point_of_sale.Printer');
    const { useRef } = owl;
    const ajax = require('web.ajax');

    const KitchenBillScreenExtend = (KitchenBillScreen) => class  extends KitchenBillScreen {
//        async sendReceiptToPrintNode() {
        //     const printer = new Printer(null, this.env.pos);
        //     const receiptString = this.orderReceipt.el.innerHTML;
        //     const ticketImage = await printer.htmlToImg(receiptString);
        //     const order = this.currentOrder;
        //     const partner = order.get_partner();
        //     const orderName = order.get_name();
        //     const order_server_id = this.env.pos.validated_orders_name_server_id_map[orderName];
        //     var result = await this.rpc({
        //         model: 'pos.order',
        //         method: 'action_receipt_to_print_node',
        //         args: [[order_server_id], order.pos_session_id, 'kitchen', ticketImage],
        //     });
        //
        //     if (result) {
        //         order.get_orderlines().forEach(function (orderline) {
        //             if (orderline.is_printed()) {
        //                 if (orderline.get_printed_total_qty() < orderline.quantity) {
        //                     orderline.set_printed_total_qty(orderline.get_printed_qty() + orderline.get_printed_total_qty());
        //                 }
        //             } else {
        //                 orderline.set_printed(true);
        //                 orderline.set_printed_total_qty(orderline.get_printed_qty());
        //             }
        //
        //         });
        //
        //         this.props.resolve({ confirmed: true, payload: null });
        //         this.trigger('close-temp-screen');
        //     }
//        }
        async sendReceiptToPrintNode() {
                const printer = new Printer(null, this.env.pos);
                const receiptString = this.orderReceipt.el.innerHTML;
                const receipt = await printer.htmlToImg(receiptString);
                ajax.jsonRpc('/km_pos_direct_print', 'call', {printer_type: 'kitchen', receipt }).then(function(data){});
//                }
            }
    };

    Registries.Component.extend(KitchenBillScreen, KitchenBillScreenExtend);
    return KitchenBillScreen;
});