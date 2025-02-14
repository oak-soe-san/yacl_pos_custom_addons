odoo.define('mscl_customer_id.CustomerIDButton', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const ProductScreen = require('point_of_sale.ProductScreen');
	const { useListener } = require("@web/core/utils/hooks");
	const Registries = require('point_of_sale.Registries');

	class CustomerIDButton extends PosComponent {
		setup() {
			super.setup();
			useListener('click', this.onClick);
		}
		async onClick() {
			const selectedOrder = this.env.pos.get_order();
               const { confirmed, payload: inputID } = await this.showPopup('TextAreaPopup', {
                    startingValue: selectedOrder.get_customer_id(),
                    title: this.env._t('Add Customer ID'),
                });
            if (confirmed) {
                selectedOrder.set_customer_id(inputID);
				console.log(inputID)
            }
		}
	}

	CustomerIDButton.template = 'CustomerIDButton';
	ProductScreen.addControlButton({
		component: CustomerIDButton,
		position : ["after" , "OrderlineCustomerNoteButton"],
	});

	Registries.Component.add(CustomerIDButton);
	return CustomerIDButton;
});