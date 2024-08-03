# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _
from datetime import datetime

class LoanInstallment(models.Model):
    _name = 'report.margin.sale'
    _description = "Loan Installment"

    name = fields.Char(string="Numero",readonly="True",compute="_compute_name")


    
    partner_id = fields.Many2one('res.partner',string="Empresa",default=lambda self : self.env.user.company_id.id,required=True)
    applied_date = fields.Date(string="Fecha",default=fields.Date.today())
    company_id = fields.Many2one('res.company' ,default=lambda self : self.env.user.company_id.id,string="Company",required=True)
    user_id = fields.Many2one('res.users',default=lambda self : self.env.user.id,string="User",readonly=True)
    principal_amount = fields.Float(string="Entrada",required=True,digits=(32, 2))
    salida = fields.Float(string="Salida",required=True,digits=(32, 2))
    balance_on_loans = fields.Float(string="Balance On Loan", store=True)
    notes = fields.Text(string="Notes")
    start_date = fields.Date(string='Fecha de Inicio', default=lambda self: fields.Date.today() - timedelta(days=30))
    end_date = fields.Date(string='Fecha de Fin', default=fields.Date.today)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    order_line = fields.One2many('report.sale.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    state = fields.Selection([('draft','Draft'),('applied','Applied'),('approve','Approved'),('closed','Cerrado'),('cancel','Cancel'),('disbursed','Disbursed')],default='draft')



    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('report.margin.sale') or '/'
        vals['name'] = seq
        return super(LoanInstallment, self).create(vals)



    def approve_payment(self):
        self.write({'state':'approve'})


    def action_payment(self):
        self._create_or_update_purchase_orders()

    def _create_or_update_purchase_orders(self):
        products = self.env['product.template'].search([])

        if not products:
            raise ValidationError(_("No hay Productos configurados."))

        
        
        for product in products:
            reorder_qty = self._get_reorder_quantity(product)
            if reorder_qty > 0:
                self._create_or_update_purchase_order_line(product, reorder_qty)
                products_updated += 1

        return self._reload_client_with_message(f'{products_updated} ordenes creadas o actualizadas correctamente.')

 

    def _get_reorder_quantity(self, product):
        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', product.id),
            ('location_id.usage', '=', 'internal'),
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('reference', 'ilike', 'WH/POS/%')
        ])
        return abs(sum(stock_moves.mapped('product_qty')))

    def _create_or_update_purchase_order_line(self, product, reorder_qty):
        purchase_order_line_obj = self.env['report.sale.line']

        purchase_order_line = purchase_order_line_obj.search([
            ('order_id', '=', self.id),
            ('product_id', '=', product.id)
        ], limit=1)

        if purchase_order_line:
            purchase_order_line.product_qty = reorder_qty
        else:
            purchase_order_line_obj.create({
                'order_id': self.id,
                'product_id': product.id,
                'name': product.name,
                'product_qty': reorder_qty,
                'product_uom': product.uom_po_id.id,
                'date_planned': fields.Date.today(),
            })


