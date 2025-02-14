from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    bar_printer_id = fields.Many2one('printer.details', string="Bar Printer")
    kitchen_printer_id = fields.Many2one('printer.details', string="Kitchen Printer")