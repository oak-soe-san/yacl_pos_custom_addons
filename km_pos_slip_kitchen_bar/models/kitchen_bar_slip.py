from odoo import fields, models

class KitchenBarSlip(models.Model):
    _name = "kitchen.bar.slip"

    name = fields.Char(string='Printer Name', required=True)
    printer_type = fields.Selection(string='Printer Type', default='bar',
        selection=[('bar', 'Bar'), ('kitchen', 'Kitchen')])
    product_categories_ids = fields.Many2many('pos.category', string='Printed Product Categories')
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company)
    active = fields.Boolean('Active', default=True)
    ip_address = fields.Char('IP Address')


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('kitchen.bar.slip')
        return result

    def _loader_params_kitchen_bar_slip(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['name', 'printer_type', 'product_categories_ids'],
            },
        }

    def _get_pos_ui_kitchen_bar_slip(self, params):
        return self.env['kitchen.bar.slip'].search_read(**params['search_params'])