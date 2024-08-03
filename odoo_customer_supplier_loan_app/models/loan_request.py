# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
import calendar
from dateutil.relativedelta import *
from odoo.exceptions import UserError, ValidationError

class LoanRequest(models.Model):
	_name = 'loan.request'
	_inherit = ['mail.thread']
	_description = "Loan Request"

	


	name = fields.Char(string="Numero",readonly=True)
	ref_loan = fields.Char(string="Referencia")
	ref_invoice = fields.Char(string="Referencia")
	partner_id = fields.Many2one('res.partner',string="Cliente",required=True,domain=[('allow_multiple_loan','=',True)])
	applied_date = fields.Date(string="Fecha",default=fields.Date.today())
	
	approve_date = fields.Date(string="Fecha de Aprobacion", required=True,default=fields.Date.today())
	disbursement_date = fields.Date(string="Fecha de Desemborso",default=fields.Date.today())
	company_id = fields.Many2one('res.company' ,default=lambda self : self.env.user.company_id.id,string="Company",required=True)
	user_id = fields.Many2one('res.users',default=lambda self : self.env.user.id,string="User",readonly=True)
	loan_partner_type = fields.Selection([('customer','Cliente'),('vendor','Supplier')],default='customer',string="Tipo de Cliente")

	entrada = fields.Boolean(string="Entrada", default=False, help="For monitoring the record")
	salir = fields.Boolean(string="Salida", default=False, help="For monitoring the record")
    #descuento = fields.Boolean(string="Salida", default=False, help="For monitoring the record")

	principal_amount = fields.Float(string="Entrada",required=True,digits=(32, 2))
	salida = fields.Float(string="Salida",required=True,digits=(32, 2))
	
	#interest_mode = fields.Selection([('flat','Flat'),('reducing','Reducing')],string="Modo de Interes")
	duration_months = fields.Integer(string="Cantidad de Cuotas",required=True,default=1)
	
	balance_on_loans = fields.Float(string="Balance On Loan", store=True)

	
	notes = fields.Text(string="Notes")

	state = fields.Selection([('draft','Draft'),('applied','Applied'),('approve','Approved'),('closed','Cerrado'),('cancel','Cancel'),('disbursed','Disbursed')],default='draft')

	
	is_compute = fields.Boolean(string="Is Compute",copy=False)
	currency_id = fields.Many2one('res.currency',string="Currency",related="company_id.currency_id")
	

	interest_mode = fields.Selection(
        [('flat', 'Abierto'), ('reducing', 'San o Cuotas')], string="Forma de pago")

	date = fields.Date(string="Fecha del Prestamo", required=True,
                       default=fields.Date.today(),
                       help="Date of the payment")



    



	def button_installment_entries(self):
		return {
			'name': _('Installment Entries'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'loan.installment',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in', self.installment_ids.ids)],
		}





	def action_confirm3(self):

		if self.salir:
			if self.partner_id.payment_amount_loan_amt != 0:
			    raise UserError("No tiene Balance para rebajar!")

		#if not self.policy_ids:
		#	raise UserError(_('Please configure or add Customer/Supplier Loan Policy..!'))
		
				
		self.write({'state':'applied'})
		self.action_approve()
		return




	def action_approve(self):
		"""
		if self.policy_ids :
			max_days = 0
			for polily in self.policy_ids :
				if polily.policy_type == 'qualifying' and polily.days > 0:
					if polily.days > max_days :
						max_days = polily.days
			if max_days > 0 :
				end_date = self.applied_date + relativedelta(days=+max_days)
				if end_date > fields.datetime.today().date() :
					raise ValidationError(_("You can approve this loan after  %s ") % end_date )
		""" 
		self.write({'state':'approve'})
		return

	def action_cancel(self):
		for statement in self:
			statement.installment_ids.unlink()
			statement.is_compute = False
		self.write({'state':'cancel'})
		return

	def reset_draft(self):
		self.write({'state':'draft'})

	def unlink(self):
		for rec in self:
			if rec.state == 'draft':
				rec.installment_ids.unlink()
		return super(LoanRequest, self).unlink()

	@api.model
	def create(self, vals):
		seq = self.env['ir.sequence'].next_by_code('loan.request') or '/'
		vals['name'] = seq
		return super(LoanRequest, self).create(vals)

	
		
	def _get_attachment_count(self):
		for loan in self:
			attachment_ids = self.env['ir.attachment'].search([('loan_request_id','=',loan.id)])
			loan.attachment_count = len(attachment_ids)

	def attachment_on_loan_button(self):
		self.ensure_one()
		return {
			'name': 'Attachment.Details',
			'type': 'ir.actions.act_window',
			'view_mode': 'tree,form',
			'res_model': 'ir.attachment',
			'domain': [('loan_request_id', '=', self.id)],
		}
		
	@api.onchange('partner_id')
	def onchange_partner(self):
		if self.partner_id.policy_ids.ids:
			self.policy_ids = self.partner_id.policy_ids.ids

	@api.onchange('loan_type_id')
	def onchange_loan_type_id(self):
		#self.interest_mode = self.loan_type_id.interest_mode
		self.rate = self.loan_type_id.rate
		return




class ReportSale(models.Model):
    _name = 'report.sale.margin'
    _description = "Report Sale Margi"

    


    name = fields.Char(string="Numero",readonly=True)
    partner_id = fields.Many2one('res.partner',string="Empresa",default=lambda self : self.env.user.company_id.id,required=True)
    applied_date = fields.Date(string="Fecha",default=fields.Date.today())
    company_id = fields.Many2one('res.company' ,default=lambda self : self.env.user.company_id.id,string="Company",required=True)
    user_id = fields.Many2one('res.users',default=lambda self : self.env.user.id,string="User",readonly=True)
    principal_amount = fields.Float(string="Entrada",required=True,digits=(32, 2))
    salida = fields.Float(string="Salida",required=True,digits=(32, 2))
    balance_on_loans = fields.Float(string="Balance On Loan", store=True)
    notes = fields.Text(string="Notes")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    order_line = fields.One2many('report.sale.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    state = fields.Selection([('draft','Draft'),('applied','Applied'),('approve','Approved'),('closed','Cerrado'),('cancel','Cancel'),('disbursed','Disbursed')],default='draft')




    def action_confirm3(self):     
        self.write({'state':'applied'})
        self.action_approve()
        return



    def action_approve(self):
        self.write({'state':'approve'})
        return

    def action_cancel(self):
        for statement in self:
            statement.installment_ids.unlink()
            statement.is_compute = False
        self.write({'state':'cancel'})
        return

    def reset_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        for rec in self:
            if rec.state == 'draft':
                rec.installment_ids.unlink()
        return super(ReportSale, self).unlink()

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('report.sale.margin') or '/'
        vals['name'] = seq
        return super(ReportSale, self).create(vals)

    def compute_loan(self):
        if not self.approve_date:
            raise UserError("You should have defined an 'Approve Date' in your Loan Request!")
        

        self.is_compute = True
        return      



class ReportSaleLine(models.Model):
    """Loan repayments """
    _name = "report.sale.line"
    _description = "Report Sale Line"

    order_id = fields.Many2one('report.sale.margin', string='Order Reference', index=True, required=True, ondelete='cascade')
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



            		
class ir_attachment(models.Model):
	_inherit='ir.attachment'

	loan_request_id  =  fields.Many2one('loan.request', 'Loan Request')
	
