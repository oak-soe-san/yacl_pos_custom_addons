from odoo import api, fields, models

class RgsGender(models.Model):
    _name = 'rgs.gender'
    _description = 'RGS Fashion Info (Gender)'

    name = fields.Char(string='Gender')

    # SQL Constraints
    _sql_constraints = [
        ('gender_uniq', 'UNIQUE(name)', 'Gender must be unique'),
    ]

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    rgs_gender_id = fields.Many2one('rgs.gender', string='Gender')