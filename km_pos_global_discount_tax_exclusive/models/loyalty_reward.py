# -*- coding: utf-8 -*-
from odoo import models

class LoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'

    def _get_discount_product_values(self):
        data = super()._get_discount_product_values()
        data[0]['is_discount_product'] = True
        data[0]['is_ewallet_product'] = True
        return data
