from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order.line'

    customer_id = fields.Char(string='Customer ID')

    @api.model
    def _export_for_ui(self, order):
        res = super(PosOrder, self)._export_for_ui(order)
        res['customer_id'] = order.customer_id
        return res

    @api.model
    def _order_fields(self, ui_order):
        # Call super to get the original result
        res = super(PosOrder, self)._order_fields(ui_order)

        # Add the new field to the result
        res['customer_id'] = ui_order.get('customer_id', '')

        return res