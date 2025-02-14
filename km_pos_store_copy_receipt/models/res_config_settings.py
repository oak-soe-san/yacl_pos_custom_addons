from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_store_copy_receipt = fields.Boolean(related='pos_config_id.is_store_copy_receipt', store=True, readonly=False)