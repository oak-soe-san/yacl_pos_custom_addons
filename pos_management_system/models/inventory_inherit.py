from odoo import _, api, fields, models


class InventoryCostInherit(models.Model):
    _inherit = 'stock.move.line'

    inventory_cost = fields.Float(
        string='Cost', related="product_id.standard_price")
    subtotal_cost = fields.Float(
        string='Sub Total', compute='_compute_sub_total_cost', store=True)
    qty_done = fields.Float('Done', default=0.0,
                            digits='Product Unit of Measure', copy=False)

    @api.depends('qty_done', 'inventory_cost')
    def _compute_sub_total_cost(self):
        for rec in self:
            if rec.qty_done and rec.inventory_cost:
                qty = rec.qty_done
                cost = rec.inventory_cost
                rec.subtotal_cost = qty * cost


class InventoryTotalCostInherit(models.Model):
    _inherit = 'stock.picking'

    move_line_ids_without_package = fields.One2many(
        domain=['&', '|', ('location_dest_id.usage', '!=', 'production'), ('move_id.picking_code', '!=', 'outgoing'),
                     '|', ('package_level_id', '=', False), ('picking_type_entire_packs', '=', False)])
    total_unit_cost = fields.Monetary(
        string='Total Cost', compute='_compute_unit_total_cost', store=True)
    discount_cost = fields.Monetary(
        string="Discount", default=0.0,)
    tax_cost = fields.Monetary(string="Tax", default=0.0,)
    delivery_cost = fields.Monetary(
        string="Delivery Cost", default=0.0,)
    currency_id = fields.Many2one(
        'res.currency', 'Currency', compute='_compute_currency_id')

    @api.depends('move_line_ids_without_package', 'discount_cost', 'tax_cost', 'delivery_cost')
    def _compute_unit_total_cost(self):
        for record in self:
            record.total_unit_cost = (((sum(rec.subtotal_cost for rec in record.move_line_ids_without_package) -
                                      record.tax_cost) - record.delivery_cost) - record.discount_cost)

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = template.company_id.sudo(
            ).currency_id.id or main_company.currency_id.id


class InventoryProductCostInherit(models.Model):
    _inherit = 'stock.move'

    inventory_cost = fields.Float(
        string='Cost', related="product_id.standard_price")
    subtotal_cost = fields.Float(
        string='Sub Total', compute='_compute_sub_total_cost', store=True)

    @api.depends('quantity_done', 'inventory_cost')
    def _compute_sub_total_cost(self):
        for rec in self:
            if rec.quantity_done and rec.inventory_cost:
                qty = rec.quantity_done
                cost = rec.inventory_cost
                rec.subtotal_cost = qty * cost
