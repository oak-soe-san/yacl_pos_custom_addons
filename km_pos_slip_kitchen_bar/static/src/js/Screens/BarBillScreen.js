odoo.define('km_pos_slip_kitchen_bar.BarBillScreen', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');
    const { useRef } = owl;
    const ajax = require('web.ajax');
    const { Printer } = require('point_of_sale.Printer');

    const BarBillScreen = (ReceiptScreen) => {
        class BarBillScreen extends ReceiptScreen {
            confirm() {
                this.props.resolve({ confirmed: true, payload: null });
                this.trigger('close-temp-screen');
            }
            whenClosing() {
                this.confirm();
            }
            /**
             * @override
             */
            async printReceipt() {
                const printer = new Printer(null, this.env.pos);
                    const receipt = await printer.htmlToImg(this.orderReceipt.el.innerHTML);
                    ajax.jsonRpc('/km_pos_slip_kitchen_bar', 'call', { receipt }).then(function(data){});
            }
        }
        BarBillScreen.template = 'BarBillScreen';
        return BarBillScreen;
    };

    Registries.Component.addByExtending(BarBillScreen, ReceiptScreen);

    return BarBillScreen;
});
