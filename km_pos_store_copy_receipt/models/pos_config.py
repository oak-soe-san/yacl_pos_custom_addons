from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_store_copy_receipt = fields.Boolean(string='Use Store Copy Receipt')