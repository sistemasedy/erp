7# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class WebSitets(http.Controller):
     @http.route('/aptes/', type='http', auth='user')
     def apps(self, **kw):
         partner = request.env['res.partner'].search([])
         products = request.env['product.template'].search([('website_published', '=', True)], limit=6)
         vals = {
            'partner': partner,
            'products': products
         }
         args = http.request.render('web_sitets.aptes', vals)
         return args
         #return http.request.render('web_sitets.aptes')



     @http.route('/tds/', type='http', auth='user')
     def tod(self, **kw):
         partner = request.env['res.partner'].search([])
         products = request.env['product.template'].search([('website_published', '=', True)], limit=6)
         vals = {
            'partner': partner,
            'products': products
         }
         args = http.request.render('web_sitets.tods', vals)
         return args



     @http.route('/inventory/', auth='public')
     def appsx(self, **kw):
         # partner = request.env['res.partner'].search([])
         # products = request.env['product.template'].search([('website_published', '=', True)], limit=6)
         # vals = {
         #    'partner': partner,
         #    'products': products
         # }
         # args = http.request.render('web_sitets.app', vals)
         # return args
         return http.request.render('web_sitets.inventorys')

     @http.route('/website/', auth='public')
     def index(self, **kw):
         return "Hello, world"

     @http.route('/list/', auth='public')
     def lists(self, **kw):
         return http.request.render('web_sitets.listing', {
             'root': '/web_sitets/web',
             'objects': http.request.env['res.partner'].search([]),
         })
     

     @http.route('/web_testing_test/<model("todo.task"):task>', auth='public', website=True)
     def test(self, task, **kw):
        vals = {
            'todo_task': task,
            'nombre': request.params['nombre']
        }
        arg = http.request.render('web_sitets.web_testing_test', vals)
        return arg

     @http.route('/create_task/todo/', type="http", auth="public", methods=['POST'], website=True)
     def create_task_todo(self, task_name, **kw):
         request.env['todo.task'].sudo().create({'name': task_name})
         task = request.env['todo.task'].search([('is_done', '=' ,False)])
         vals = {
            'todo_task': task
         }
         args = http.request.render('web_sitets.web_testing_tests', vals)
         return args

     @http.route('/edy/', auth='public', website=True)
     def tests(self, **kw):
         partner = request.env['res.partner'].search([])
         products = request.env['product.template'].search([('website_published', '=', True)], limit=6)
         vals = {
            'partner': partner,
            'products': products
         }
         args = http.request.render('web_sitets.edy', vals)
         return args

     @http.route('/task/new', type='http', auth="public", methods=['POST'], website=True)
     def forum_create(self, forum_name="New Forum"):
         request.env['todo.task'].sudo().create({'name': forum_name})
         
         return request.redirect("/web_testing_tests/")





     @http.route('/task/<int:task_id>/todo/new', type='http', auth="public", website=True)
     def post_create(self, task_id, **todo):
         new_todo_task = request.env['todo.task'].create({
             'task_id': task_id,
             'name': 'odoo',
         })
         return werkzeug.utils.redirect()



     

     

     @http.route('/create_task/', auth='public', type='json', website=True)
     def create_task(self, **rec):
        if request.jsonrequest:
            print("rec", rec)
            if rec['name']:
                vals = {
                     'task_name': rec['name']
                }
                new_task = request.env['todo.task'].sudo().create(vals)
                print("New Task", new_task)
                args = {'success': True, 'message': 'Success', 'id': new_task.id}
        return args


     



     


     @http.route('/sitio/', auth='public', website=True)
     def sitios(self, **kw):
         return http.request.render('web_sitets.sitio')

     @http.route('/plantilla/', auth='public', website=True)
     def plantillas(self, **kw):
         return http.request.render('web_sitets.plantilla')



     @http.route('/customer', auth='public', website=True)
     def customer(self, **kw):
         return http.request.render('web_sitets.web_customer')

     @http.route('/customer_web/customer_web/objects/', auth='public', website=True)
     def list(self, **kw):
         return http.request.render('customer_web.res_partner', {
             'root': '/customer_web/customer_web',
             'objects': http.request.env['web_sitets.web_testing_test'].search([]),
         })

     @http.route(['/get_products'], type='json', auth="public", website=True)
     def get_products(self):
         products = request.env['product.template'].search([('website_published', '=', True)], limit=6)
         p = []

         for product in products:
             news  = {
                   "name": product.name,
                   "list_price": product.list_price
             }
             p.append(news)

         return p