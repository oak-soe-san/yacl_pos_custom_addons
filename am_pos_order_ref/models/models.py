# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, Warning
from odoo.http import request
from functools import partial
import datetime
import logging
import re

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    pos_order_ref = fields.Char(string='Order Name', required=False)
    pos_orders_count = fields.Integer(default = 0)

    def _get_fields_for_draft_order(self):
        #print('_get_fields_for_draft_order call')
        fields = super(PosOrder, self)._get_fields_for_draft_order()
        fields.extend([
            'pos_order_ref',
            'pos_orders_count'
        ])
        return fields

    @api.model
    def _order_fields(self, ui_order):
        #print('_order_fields call ', ui_order)
        vals = super(PosOrder, self)._order_fields(ui_order)
        vals['pos_order_ref'] = ui_order['pos_order_ref']
        vals['pos_orders_count'] = ui_order['pos_orders_count']
        return vals

    def _compute_order_name(self):
        if len(self.refunded_order_ids) != 0:
            return ','.join(self.refunded_order_ids.mapped('name')) + _(' REFUND')
        else:
            #print("pos_orders_count", self.pos_orders_count)
            for i in range(self.pos_orders_count):
                ii = self.session_id.config_id.sequence_id._next()

            return self.pos_order_ref

    @api.model
    def update_order_ref(self,sequence_id):
        if sequence_id:
            sequence_id = self.env['ir.sequence'].browse(sequence_id)

            return sequence_id.number_next_actual
