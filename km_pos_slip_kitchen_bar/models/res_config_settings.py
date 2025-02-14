from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_kitchen_bar_slip = fields.Boolean(related='pos_config_id.is_kitchen_bar_slip', store=True, readonly=False)