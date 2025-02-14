odoo.define('bi_pos_multi_receipt.CustomAbstractReceiptScreen', function(require) {
    'use strict';

    const AbstractReceiptScreen = require('point_of_sale.AbstractReceiptScreen');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    var EpsonPrinter = require('pos_epson_printer.Printer');
    var core = require('web.core');
    var QWeb = core.qweb;
    const { useRef } = owl;
    const { nextFrame } = require('point_of_sale.utils');


    const CustomAbstractReceiptScreen = (AbstractReceiptScreen) =>
    class extends AbstractReceiptScreen {
        setup() {
            super.setup();
            this.orderReceipt = useRef('order-receipt');
		}
        async _printReceipt() {
            if (this.env.proxy.printer) {
                if(this.env.pos.config.print_multi_receipt){
                    for (let copies = 1; copies <= this.env.pos.config.no_of_receipt; copies++) {
                        const printResult = await this.env.proxy.printer.print_receipt(this.orderReceipt.el.innerHTML);
                    }
                    if (printResult.successful) {
                        return true;
                    } else {
                        const { confirmed } = await this.showPopup('ConfirmPopup', {
                            title: printResult.message.title,
                            body: 'Do you want to print using the web printer?',
                        });
                        if (confirmed) {
                            await nextFrame();
                            return await this._printWeb();
                        }
                        return false;
                    }
                }else{
                    const printResult = await this.env.proxy.printer.print_receipt(this.orderReceipt.el.innerHTML);
                    if (printResult.successful) {
                        return true;
                    } else {
                        const { confirmed } = await this.showPopup('ConfirmPopup', {
                            title: printResult.message.title,
                            body: 'Do you want to print using the web printer?',
                        });
                        if (confirmed) {
                            await nextFrame();
                            return await this._printWeb();
                        }
                        return false;
                    }
                }
            } else {
                return await this._printWeb();
            }
        }
    }
    Registries.Component.extend(AbstractReceiptScreen, CustomAbstractReceiptScreen);
    return AbstractReceiptScreen;
});