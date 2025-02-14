from odoo import _, api, fields, models


class YACLMultiContact(models.Model):
    _inherit = 'res.partner'

    # company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
    #     default=lambda self: self.env.company)