odoo.define('km_pos_currency.MultiCurrencyScreen', function (require) {
	'use strict';

	const ReceiptScreen = require('point_of_sale.ReceiptScreen');
	const Registries = require('point_of_sale.Registries');

	const MultiCurrencyScreen = (ReceiptScreen) => {
		class MultiCurrencyScreen extends ReceiptScreen {
			setup() {
	            super.setup();
				this.state = {
	                currency: this.props.currency
	            };
        	}

			confirm() {
				this.props.resolve({ confirmed: true, payload: null });
				this.trigger('close-temp-screen');
			}
			
			whenClosing() {
				this.confirm();
			}

			async printReceipt() {
				await super.printReceipt();
				this.currentOrder._printed = false;
			}
		}

		MultiCurrencyScreen.template = 'MultiCurrencyScreen';
		return MultiCurrencyScreen;
	};

	Registries.Component.addByExtending(MultiCurrencyScreen, ReceiptScreen);
	return MultiCurrencyScreen;
});