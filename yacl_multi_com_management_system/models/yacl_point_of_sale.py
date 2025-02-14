from odoo import _, api, fields, models



class YACLMultiProduct(models.Model):
    _inherit = 'product.template'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)



class YACLMultiPOSProductCategory(models.Model):
    _inherit = 'pos.category'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)



class YACLMultiPOSBill(models.Model):
    _inherit = 'pos.bill'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)



class YACLMultiFloor(models.Model):
    _inherit = 'restaurant.floor'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)



class YACLMultiAttributes(models.Model):
    _inherit = 'product.attribute'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)



class YACLMultiPrinter(models.Model):
    _inherit = 'restaurant.printer'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)