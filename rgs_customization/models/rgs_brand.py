from odoo import api, fields, models

class RgsBrand(models.Model):
    _name = 'rgs.brand'
    _description = 'RGS Fashion Info (Brand)'

    name = fields.Char('RGS Brand', required=True)

    # SQL Constraints
    _sql_constraints = [
        ('brand_uniq', 'UNIQUE(name)', 'Brand name must be unique'),
    ]


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    rgs_brand_id = fields.Many2one('rgs.brand', string='RGS Brand', required=False)


