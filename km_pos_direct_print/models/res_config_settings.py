from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_bar_printer_id = fields.Many2one(related='pos_config_id.bar_printer_id', store=True, readonly=False)
    pos_kitchen_printer_id = fields.Many2one(related='pos_config_id.kitchen_printer_id', store=True, readonly=False)