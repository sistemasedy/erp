# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _
from datetime import datetime

class LoanInstallment(models.Model):
    _name = 'loan.installment'
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
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    order_line = fields.One2many('report.sale.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    state = fields.Selection([('draft','Draft'),('applied','Applied'),('approve','Approved'),('closed','Cerrado'),('cancel','Cancel'),('disbursed','Disbursed')],default='draft')




   
    

    def approve_payment(self):
        self.write({'state':'approve'})



  

   


    def action_payment(self):
        #if self.invoice_image:




   

    def reset_draft(self):
        self.write({'state':'unpaid'})

   
    def book_interest(self):
        pass


