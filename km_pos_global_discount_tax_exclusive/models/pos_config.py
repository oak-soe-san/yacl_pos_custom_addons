from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_global_discount_tax_exclusive = fields.Boolean(string='Use Global Discount Tax Exclusive')