# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class yacl_multi_com_management_system(models.Model):
#     _name = 'yacl_multi_com_management_system.yacl_multi_com_management_system'
#     _description = 'yacl_multi_com_management_system.yacl_multi_com_management_system'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
