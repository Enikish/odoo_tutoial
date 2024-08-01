# -*- coding: utf-8 -*-
# from odoo import http


# class SaleExtend(http.Controller):
#     @http.route('/sale_extend/sale_extend', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_extend/sale_extend/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_extend.listing', {
#             'root': '/sale_extend/sale_extend',
#             'objects': http.request.env['sale_extend.sale_extend'].search([]),
#         })

#     @http.route('/sale_extend/sale_extend/objects/<model("sale_extend.sale_extend"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_extend.object', {
#             'object': obj
#         })

