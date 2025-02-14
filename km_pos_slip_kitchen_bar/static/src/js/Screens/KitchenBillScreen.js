odoo.define('km_pos_slip_kitchen_bar.KitchenBillScreen', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const KitchenBillScreen = (ReceiptScreen) => {
        class KitchenBillScreen extends ReceiptScreen {
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
                await super.printReceipt();
                this.currentOrder._printed = false;
            }
        }
        KitchenBillScreen.template = 'KitchenBillScreen';
        return KitchenBillScreen;
    };

    Registries.Component.addByExtending(KitchenBillScreen, ReceiptScreen);

    return KitchenBillScreen;
});
