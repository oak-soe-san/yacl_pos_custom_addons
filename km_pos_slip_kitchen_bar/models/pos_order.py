from odoo import models, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    bar_button = fields.Boolean('Bar Button')
    kitchen_button = fields.Boolean('Kitchen Button')