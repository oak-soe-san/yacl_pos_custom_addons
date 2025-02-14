odoo.define('bi_pos_multi_receipt.CustomReceiptScreen', function(require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    var EpsonPrinter = require('pos_epson_printer.Printer');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;

    const CustomReceiptScreen = (ReceiptScreen) =>
    class extends ReceiptScreen {
        setup() {
            super.setup();
            this.state = {
				receipt_no_count: [] || false,
			};
            if (this.env.pos.config.print_multi_receipt) {
                for (let copies = 1; copies <= this.env.pos.config.no_of_receipt; copies++) {
                    this.state.receipt_no_count.push(copies);
                }
            }
        }
    }
    Registries.Component.extend(ReceiptScreen, CustomReceiptScreen);
    return ReceiptScreen;
});