odoo.define('pos_reports_omax.pos_session_pl_report_omax', function (require) {
    "use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    const core = require('web.core');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require("@web/core/utils/hooks");
    const { ConnectionLostError, ConnectionAbortedError } = require('@web/core/network/rpc_service')
    const { identifyError } = require('point_of_sale.utils');

    var QWeb = core.qweb;
        
    class PLSessionReportPrintButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        async onClick() {
            var self = this.env;
            var pos_session_id = self.pos.pos_session.id;
            self.legacyActionManager.do_action(
                'pos_reports_omax.action_report_session_pl', {
                    additional_context: {active_ids: [pos_session_id]},
                });
        }
    }
    PLSessionReportPrintButton.template = 'PLSessionReportPrintButton';
    ProductScreen.addControlButton({
        component: PLSessionReportPrintButton,
        condition: function () {
            return this.env.pos.config.omax_session_pl_report
        },
    });
    Registries.Component.add(PLSessionReportPrintButton);

    return PLSessionReportPrintButton;
    
});
