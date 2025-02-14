odoo.define('km_pos_currency.MultiCurrencyButton', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const ProductScreen = require('point_of_sale.ProductScreen');
	const { useListener } = require("@web/core/utils/hooks");
	const Registries = require('point_of_sale.Registries');

	class MultiCurrencyButton extends PosComponent {
		setup() {
			super.setup();
			useListener('click', this.onClick);
		}

		async onClick() {
			const order = this.env.pos.get_order();
			if (order.get_orderlines().length > 0) {
                const currencyList = this.env.pos.multicurrencypayment
                    .map((currency) => {
                        return {
                            id: currency.id,
                            item: currency,
                            label: currency.name,
                            isSelected: false,
                        };
                    });

                let {confirmed, payload: currency} = await this.showPopup('SelectionPopup', {
                    title: this.env._t('Change Currency'),
                    list: currencyList,
                });

                if (!confirmed) {
                    return;
                }

                if (currency) {
                    await this.showTempScreen('MultiCurrencyScreen', { currency: currency });
                }
			} else {
				await this.showPopup('ErrorPopup', {
					title: this.env._t('Nothing to Print'),
					body: this.env._t('There are no order lines'),
				});
			}
		}
	}

	MultiCurrencyButton.template = 'MultiCurrencyButton';
	ProductScreen.addControlButton({
		component: MultiCurrencyButton,
		condition: function() {
			return this.env.pos.config.multi_currency_payment;
		},
	});

	Registries.Component.add(MultiCurrencyButton);
	return MultiCurrencyButton;
});