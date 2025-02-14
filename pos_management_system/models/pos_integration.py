from odoo import _, api, fields, models


class IZELPOSIntegration(models.Model):
    _name = 'izel.pos.integration'
    _description = 'IZEL POS Integration'

    name = fields.Many2one('pos.config', string="POS Name")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    tp_session_id = fields.Char(string="Session ID")
    order_qty = fields.Float(string="Order Qty")
    discount_qty = fields.Float(string="Discount Qty")
    price_subtotal = fields.Monetary(
        string="Subtotal w/o Tax")
    price_subtotal_incl = fields.Monetary(
        string="Subtotal")
    amount_tax = fields.Monetary(string="Tax Amount")
    amount_total = fields.Monetary(string="Total")
    currency_id = fields.Many2one('res.currency', ondelete="restrict")
    company_id = fields.Many2one('res.company', string='Company', required=False, readonly=False,
        default=lambda self: self.env.company)
