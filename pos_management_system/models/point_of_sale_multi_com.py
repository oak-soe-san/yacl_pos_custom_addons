from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class POSMultiProduct(models.Model):
    _inherit = 'product.template'

    is_discount_product = fields.Boolean('Discount Product', default=False)
    is_discount_label = fields.Boolean('Discount Label', default=False)
    company_id = fields.Many2one('res.company', string='Company', required=False, readonly=False,
                                 default=lambda self: self.env.company)


class POSMultiPOSProductCategory(models.Model):
    _inherit = 'pos.category'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)


class POSMultiPOSBill(models.Model):
    _inherit = 'pos.bill'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)


class POSMultiFloor(models.Model):
    _inherit = 'restaurant.floor'

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)


class POSSessionZ(models.Model):
    _inherit = 'pos.session'

    session_z_product = fields.Boolean(
        string='Session Z Product Report', default=True)
    session_z_product_tax_exclusive = fields.Boolean(
        string='Session Z Product Tax Exclusive Report', default=False)

    @api.onchange('session_z_product_tax_exclusive')
    def onchange_tax_exclusive(self):
        for rec in self:
            if rec.session_z_product_tax_exclusive == True:
                rec.session_z_product = False
            if rec.session_z_product_tax_exclusive == False:
                rec.session_z_product = True

    @api.constrains('session_z_product_tax_exclusive', 'session_z_product')
    def _check_tax_exclusive(self):
        for rec in self:
            if rec.session_z_product_tax_exclusive and rec.session_z_product:
                raise ValidationError(
                    "You Cannot enable both Session Z Product and Session Z Product Tax Exclusive at the same time.")


class IZELPosConfig(models.Model):
    _inherit = 'pos.config'

    pos_pos_receipt = fields.Boolean(
        string="Remove Order Reference", default=True)


class IZELResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_pos_receipt = fields.Boolean(
        string="Remove Order Reference", related='pos_config_id.pos_pos_receipt', readonly=False, default=True)
