from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.template'

    is_discount_product = fields.Boolean('Is Discount Product')
    is_ewallet_product = fields.Boolean('Is eWallet Product', readonly=True)