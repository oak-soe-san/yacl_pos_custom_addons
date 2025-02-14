# -*- coding: utf-8 -*-
# from odoo import http


# class YaclMultiComManagementSystem(http.Controller):
#     @http.route('/yacl_multi_com_management_system/yacl_multi_com_management_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/yacl_multi_com_management_system/yacl_multi_com_management_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('yacl_multi_com_management_system.listing', {
#             'root': '/yacl_multi_com_management_system/yacl_multi_com_management_system',
#             'objects': http.request.env['yacl_multi_com_management_system.yacl_multi_com_management_system'].search([]),
#         })

#     @http.route('/yacl_multi_com_management_system/yacl_multi_com_management_system/objects/<model("yacl_multi_com_management_system.yacl_multi_com_management_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('yacl_multi_com_management_system.object', {
#             'object': obj
#         })
