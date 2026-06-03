# -*- coding: utf-8 -*-
from odoo import http

# class EmProduct(http.Controller):
#     @http.route('/em_product/em_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/em_product/em_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('em_product.listing', {
#             'root': '/em_product/em_product',
#             'objects': http.request.env['em_product.em_product'].search([]),
#         })

#     @http.route('/em_product/em_product/objects/<model("em_product.em_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('em_product.object', {
#             'object': obj
#         })