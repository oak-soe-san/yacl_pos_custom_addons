# -*- coding: utf-8 -*-
# from odoo import http


# class PosManagementSystem(http.Controller):
#     @http.route('/pos_management_system/pos_management_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_management_system/pos_management_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_management_system.listing', {
#             'root': '/pos_management_system/pos_management_system',
#             'objects': http.request.env['pos_management_system.pos_management_system'].search([]),
#         })

#     @http.route('/pos_management_system/pos_management_system/objects/<model("pos_management_system.pos_management_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_management_system.object', {
#             'object': obj
#         })
