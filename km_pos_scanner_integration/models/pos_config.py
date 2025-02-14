from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_passport_scanner = fields.Boolean(string='Use Passport Scanner')