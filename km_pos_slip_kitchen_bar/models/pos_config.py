from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_kitchen_bar_slip = fields.Boolean(string='Use Kitchen and Bar Slip')