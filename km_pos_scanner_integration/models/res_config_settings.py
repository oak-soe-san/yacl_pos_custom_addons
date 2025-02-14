from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_passport_scanner = fields.Boolean(related='pos_config_id.is_passport_scanner', readonly=False)