odoo.define('km_pos_slip_kitchen_bar.BillBarButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

    class BillBarButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }

        async onClick() {
            const order = this.env.pos.get_order();
            if (order.get_orderlines().length > 0) {
                await this.showTempScreen('BarBillScreen');
            } else {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Nothing to Print'),
                    body: this.env._t('There are no order lines'),
                });
            }
        }
    }

    BillBarButton.template = 'BillBarButton';

    ProductScreen.addControlButton({
        component: BillBarButton,
        condition: function() {
            return this.env.pos.config.is_kitchen_bar_slip;
        },
    });
        
    Registries.Component.add(BillBarButton);

    return BillBarButton;
});
