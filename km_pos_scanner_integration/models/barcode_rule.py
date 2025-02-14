from odoo import api, fields, models


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(
        selection_add=[
            ('passport', 'Passport')
        ], ondelete={
            'passport': 'set default'
        })