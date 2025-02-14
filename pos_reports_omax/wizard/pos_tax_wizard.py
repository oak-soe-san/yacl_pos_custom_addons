# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import Counter

from odoo import api, fields, models ,SUPERUSER_ID
import time
from datetime import datetime
from odoo.exceptions import UserError ,ValidationError

class POSTaxWizard(models.TransientModel):
    _name = 'pos.tax.wizard'
    _description = 'Point Of Sale Report'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    company_ids = fields.Many2many('res.company', string="Company")
    user_ids = fields.Many2many('res.users', string="Users")
    pos_config_ids = fields.Many2many('pos.config', string="Point Of Sale")

    def print_pos_tax_receipt(self):
        if self.end_date < self.start_date:
            raise ValidationError('End Date must be greater than or equals to Start Date !')
        self.ensure_one()
        data = {}
        data['form'] = self.read(['start_date', 'end_date','company_ids'])[0]
        return self.env.ref('pos_reports_omax.action_pos_tax_receipt_print').report_action(self, data=data)
