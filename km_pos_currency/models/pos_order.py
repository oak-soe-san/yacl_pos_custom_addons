# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    final_change = fields.Char(string='Final Change')

    @api.model
    def _order_fields(self, ui_order):
        vals = super(PosOrder, self)._order_fields(ui_order)
        if 'final_change' in ui_order:
            vals['final_change'] = ui_order['final_change'] or False
        return vals