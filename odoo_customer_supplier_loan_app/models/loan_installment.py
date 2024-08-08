# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, datetime

class LoanInstallment(models.Model):
    _name = 'loan.installment'
    _description = "Loan Installment"

    name = fields.Char(string="Numero",readonly="True" ,default='NUEMERO')

    partner_id = fields.Many2one('res.partner',string="Empresa",default=lambda self : self.env.user.company_id.id,required=True)
    applied_date = fields.Date(string="Fecha",default=fields.Date.today())
    company_id = fields.Many2one('res.company' ,default=lambda self : self.env.user.company_id.id,string="Company",required=True)
    user_id = fields.Many2one('res.users',default=lambda self : self.env.user.id,string="User",readonly=True)
    principal_amount = fields.Float(string="Entrada", digits=(32, 2))
    salida = fields.Float(string="Salida", digits=(32, 2))
    balance_on_loans = fields.Float(string="Balance On Loan", store=True)
    notes = fields.Text(string="Notes")
    start_date = fields.Date(string='Fecha de Inicio', default=lambda self: fields.Date.today() - timedelta(days=30))
    end_date = fields.Date(string='Fecha de Fin', default=fields.Date.today)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    order_line = fields.One2many('report.sale.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    
    state = fields.Selection([('unpaid','Pendiente'),('approve','Aprovado'),('paid','Pagado')],default='unpaid',string="Estado")
    


    mora = fields.Float(string="Mora", help="Amount",
                        digits=(16, 2))
    sum_parcial = fields.Float(string="Suma Parcial", help="Amount",
                               digits=(16, 2))
    suma_inte = fields.Float(string="Mora", help="Amount",
                             digits=(16, 2))

    anterior_interes = fields.Float(string="I Anterior", help="Amount",
                                    digits=(16, 2))

    sum_paid = fields.Float(string="Pagos", help="Amount",
                            digits=(16, 2))

    sum_paid_int = fields.Float(string="Interes Pagado", help="Amount",
                                digits=(16, 2))
    sum_int_pendiente = fields.Float(string="Intereses Pendiente", help="Amount",
                                     digits=(16, 2))

   

    def approve_payment(self):
        self.write({'state':'approve'})



    

    def action_payment(self):
        self._create_or_update_purchase_orders()

    def _create_or_update_purchase_orders(self):
        products = self.env['product.template'].search([])

        if not products:
            raise ValidationError(_("No hay Productos configurados."))

        
        products_updated = 0
        for product in products:
            reorder_qty = self._get_reorder_quantity(product)
            if reorder_qty > 0:
                self._create_or_update_purchase_order_line(product, reorder_qty)
                products_updated += 1

        return self._reload_client_with_message(f'{products_updated} ordenes creadas o actualizadas correctamente.')

 

    

    def _reload_client_with_message(self, message):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'name': 'Productos Actualizados',
            'params': {'message': message}
        }




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
                'price_unit': product.list_price,
                'name': product.name,
                'product_qty': reorder_qty,
                'product_uom': product.uom_po_id.id,
            })
        




    
   

    def reset_draft(self):
        self.write({'state':'unpaid'})

   
    def book_interest(self):
        pass






class ReportSaleLine(models.Model):
    """Loan repayments """
    _name = "report.sale.line"
    _description = "Report Sale Line"

    name = fields.Char(string="Descripcion")
    order_id = fields.Many2one('loan.installment', string='Order Reference', index=True, required=True, ondelete='cascade')
    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True)
    product_uom_qty = fields.Float(string='Total Quantity', compute='_compute_product_uom_qty', store=True)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True)
    product_type = fields.Selection(related='product_id.detailed_type', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')

    currency_id = fields.Many2one('res.currency', related='order_id.currency_id', store=True, readonly=True, string='Currency')
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True, currency_field='currency_id')
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True, currency_field='currency_id')

    company_id = fields.Many2one('res.company', related='order_id.company_id', string='Company', store=True, readonly=True)
    state = fields.Selection(related='order_id.state', store=True)

    partner_id = fields.Many2one('res.partner', related='order_id.partner_id', string='Partner', readonly=True, store=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.product_qty * line.price_unit
            line.price_total = line.price_subtotal



