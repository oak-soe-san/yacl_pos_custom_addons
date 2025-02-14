# -*- coding: utf-8 -*-
from odoo import models, api


class PosPayment(models.Model):
    _inherit = 'pos.payment'

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if 'is_change' in val:
                pos_order = self.env['pos.order'].browse(val['pos_order_id'])
                if val['is_change'] and pos_order.session_id.config_id.multi_currency_payment:
                    final_change = pos_order.final_change
                    if final_change:
                        val['currency_amount_total'] = float(final_change[final_change.find(' ') + 1 :])
                        val['selected_currency_symbol'] = str(final_change[:final_change.find(' ')])
        order = super().create(vals_list)
        return order