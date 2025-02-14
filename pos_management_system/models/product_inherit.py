from odoo import _, api, fields, models


class BarcodeProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Remove Barcode Unique Function'

    @api.constrains('barcode')
    def _check_barcode_uniqueness(self):
        """ With GS1 nomenclature, products and packagings use the same pattern. Therefore, we need
        to ensure the uniqueness between products' barcodes and packagings' ones"""
        None


class IZELProductTemplate(models.Model):
    _inherit = 'product.template'

    shop_name_id = fields.Char(string="Shop Name")
    room_number_id = fields.Char(string="Room Number")
    sub_catg_id = fields.Char(string="Sub Category")
    department_id = fields.Many2one('izel.product.department', string="Department")
    color_id = fields.Char(string="Color")
    size_id = fields.Char(string="Size")
    season_id = fields.Many2one('izel.product.season', string="Season")
    additional_info_id = fields.Boolean(string="Additional Information")
 

class IZELProductDepartment(models.Model):
    _name = 'izel.product.department'
    _description = 'IZEL Product Department'

    name=fields.Char(string="Department Name")
    company_id = fields.Many2one('res.company', string='Company', required=False, readonly=False,
        default=lambda self: self.env.company)
    


class IZELProductSeason(models.Model):
    _name = 'izel.product.season'
    _description = 'IZEL Product Season'

    name=fields.Char(string="Season Name")
    company_id = fields.Many2one('res.company', string='Company', required=False, readonly=False,
        default=lambda self: self.env.company)