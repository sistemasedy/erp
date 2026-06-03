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

		
class ir_attachment(models.Model):
	_inherit='ir.attachment'

	loan_request_id  =  fields.Many2one('loan.request', 'Loan Request')
	
