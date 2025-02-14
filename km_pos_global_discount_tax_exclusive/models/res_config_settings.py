from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_global_discount_tax_exclusive = fields.Boolean(related='pos_config_id.is_global_discount_tax_exclusive', store=True, readonly=False)