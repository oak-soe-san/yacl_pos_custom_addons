odoo.define('pos_reports_omax.PosLogoBarcode', function (require) {
    "use strict";
    
    const Registries = require('point_of_sale.Registries');
    const OrderReceipt = require('point_of_sale.OrderReceipt');
	
    const PosLogoBarcode = (OrderReceipt) =>
        class extends OrderReceipt {
                get receipt() {
                    var order = this.receiptEnv.order;
                    var ordername = "Order "+order.uid;
                    this.receiptEnv.receipt['company']['street']= this.receiptEnv.order.pos['company']['street'];
                    this.receiptEnv.receipt['company']['street2']= this.receiptEnv.order.pos['company']['street2'];
                    this.receiptEnv.receipt['company']['city']= this.receiptEnv.order.pos['company']['city'];
                    this.receiptEnv.receipt['company']['state_id']= this.receiptEnv.order.pos['company']['state_id'];
                    this.receiptEnv.receipt['company']['country_id']= this.receiptEnv.order.pos['company']['country_id'];
                    this.receiptEnv.receipt['company']['zip']= this.receiptEnv.order.pos['company']['zip'];
                    return this.receiptEnv.receipt;
                }
        };
    Registries.Component.extend(OrderReceipt, PosLogoBarcode);
    return OrderReceipt;
});
