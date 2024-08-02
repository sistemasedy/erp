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
    partner_id = fields.Many2one('res.partner',string="Cliente",required=True)
    applied_date = fields.Date(string="Fecha",default=fields.Date.today())
    
    approve_date = fields.Date(string="Fecha de Aprobacion", required=True,default=fields.Date.today())
    disbursement_date = fields.Date(string="Fecha de Desemborso",default=fields.Date.today())
    company_id = fields.Many2one('res.company' ,default=lambda self : self.env.user.company_id.id,string="Company",required=True)
    user_id = fields.Many2one('res.users',default=lambda self : self.env.user.id,string="User",readonly=True)
    loan_partner_type = fields.Selection([('customer','Cliente'),('vendor','Supplier')],default='customer',string="Tipo de Cliente")

    entrada = fields.Boolean(string="Entrada", default=False, help="For monitoring the record")
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

        #if not self.policy_ids:
        #   raise UserError(_('Please configure or add Customer/Supplier Loan Policy..!'))
        
                
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

    def compute_loan(self):
        if not self.approve_date:
            raise UserError("You should have defined an 'Approve Date' in your Loan Request!")
        month = self.approve_date.month
        year = self.approve_date.year
        
        month_principal_amount = self.principal_amount / self.duration_months
        
        #total_interest_amount = (self.principal_amount * self.rate * self.duration_months) / (12 * 100)
        total_interest_amount = (self.principal_amount * self.rate) / 100
        interest_amount = total_interest_amount / self.duration_months
        
        installment_obj = self.env['loan.installment']
        installment_list = []

        months = self.duration_months
        amount_to_pay = self.principal_amount 

        common_rate = self.rate
        duration_months_change = self.duration_months
        opening_balance_change = self.principal_amount
        if self.loan_type_id.tenure_plan == 'week':
            date_start = (datetime.strptime(str(self.date),'%Y-%m-%d') + relativedelta(weeks=1))

            for number in range(1,self.duration_months+1):

                
                month_principal_amount = round(month_principal_amount, 2)
                interest_amount = round(interest_amount, 2)
                principal_ending_balance = opening_balance_change  - month_principal_amount
                principal_ending_balance = round(principal_ending_balance, 2)
                if number == (self.duration_months):
                    month_principal_amount = month_principal_amount + principal_ending_balance
                    principal_ending_balance = opening_balance_change - month_principal_amount
                    principal_ending_balance = round(abs(principal_ending_balance), 2)

                vals = {
                    'loan_id' : self.id ,
                    'partner_id':self.partner_id.id,
                    'opening_balance_amount': opening_balance_change,
                    'principal_amount': month_principal_amount,
                    'interest_amount':  interest_amount,
                    'emi_installment' : month_principal_amount + interest_amount,
                    'ending_balance_amount' : principal_ending_balance,
                    'state' : 'unpaid',
                    'currency_id' : self.company_id.currency_id.id,
                    'loan_type_id' : self.loan_type_id.id ,
                    'installment_number' : number,
                    'date' : date_start,
                    'date_from' : date_start,'date_to' : date_start,
                    'loan_partner_type' : self.loan_partner_type,
                    }
                installment  = installment_obj.create(vals)
                opening_balance_change = principal_ending_balance
                duration_months_change = duration_months_change - 1
                date_start += relativedelta(weeks=1)

            
            installment_list.append(installment.id)


        if self.loan_type_id.tenure_plan == 'fortnight':
            date_start = (datetime.strptime(str(self.date),'%Y-%m-%d') + relativedelta(days=15))

            for number in range(1,self.duration_months+1):

                
                month_principal_amount = round(month_principal_amount, 2)
                interest_amount = round(interest_amount, 2)
                principal_ending_balance = opening_balance_change  - month_principal_amount
                principal_ending_balance = round(principal_ending_balance, 2)
                if number == (self.duration_months):
                    month_principal_amount = month_principal_amount + principal_ending_balance
                    principal_ending_balance = opening_balance_change - month_principal_amount
                    principal_ending_balance = round(abs(principal_ending_balance), 2)

                vals = {
                    'loan_id' : self.id ,
                    'partner_id':self.partner_id.id,
                    'opening_balance_amount': opening_balance_change,
                    'principal_amount': month_principal_amount,
                    'interest_amount':  interest_amount,
                    'emi_installment' : month_principal_amount + interest_amount,
                    'ending_balance_amount' : principal_ending_balance,
                    'state' : 'unpaid',
                    'currency_id' : self.company_id.currency_id.id,
                    'loan_type_id' : self.loan_type_id.id ,
                    'installment_number' : number,
                    'date' : date_start,
                    'date_from' : date_start,'date_to' : date_start,
                    'loan_partner_type' : self.loan_partner_type,
                    }
                installment  = installment_obj.create(vals)
                opening_balance_change = principal_ending_balance
                duration_months_change = duration_months_change - 1
                date_start += relativedelta(days=15)

            
            installment_list.append(installment.id)


        if self.loan_type_id.tenure_plan == 'monthly':
            date_start = (datetime.strptime(str(self.date),'%Y-%m-%d') + relativedelta(months=1))

            for number in range(1,self.duration_months+1):

                
                month_principal_amount = round(month_principal_amount, 2)
                interest_amount = round(interest_amount, 2)
                principal_ending_balance = opening_balance_change  - month_principal_amount
                principal_ending_balance = round(principal_ending_balance, 2)
                if number == (self.duration_months):
                    month_principal_amount = month_principal_amount + principal_ending_balance
                    principal_ending_balance = opening_balance_change - month_principal_amount
                    principal_ending_balance = round(abs(principal_ending_balance), 2)

                vals = {
                    'loan_id' : self.id ,
                    'partner_id':self.partner_id.id,
                    'opening_balance_amount': opening_balance_change,
                    'principal_amount': month_principal_amount,
                    'interest_amount':  interest_amount,
                    'emi_installment' : month_principal_amount + interest_amount,
                    'ending_balance_amount' : principal_ending_balance,
                    'state' : 'unpaid',
                    'currency_id' : self.company_id.currency_id.id,
                    'loan_type_id' : self.loan_type_id.id ,
                    'installment_number' : number,
                    'date' : date_start,
                    'date_from' : date_start,'date_to' : date_start,
                    'loan_partner_type' : self.loan_partner_type,
                    }
                installment  = installment_obj.create(vals)
                opening_balance_change = principal_ending_balance
                duration_months_change = duration_months_change - 1
                date_start += relativedelta(months=1)

            
            installment_list.append(installment.id)




        self.is_compute = True
        return      


   

 

 

    def disburse_loan(self):

        if not self.applied_date:
            raise UserError("You should have defined an 'Applied Date' in your Loan Request!")

        for line in self.installment_ids : 
            if self.loan_type_id.repayment_method == "direct" :
                line.pay_from_payroll = True

            elif self.loan_type_id.repayment_method == "payroll" :
                line.pay_from_payroll = False

        account_move = self.env['account.move']

        name_of = self.partner_id.name
        
        if not self.partner_account_id:
            raise ValidationError(("Please configure partner account in loan system..!"))

        if not self.disburse_journal_id.available_payment_method_ids:
            raise ValidationError(("Please configure payment credit account from disburse journal in loan system..!"))

        debit_line = [0,0,{'account_id' : self.partner_account_id.id,
                            'partner_id' : self.user_id.partner_id.id,
                            'name' : 'Loan Of ' + name_of,
                            'debit' : 0.0,
                            'credit' : self.principal_amount
                            }]

        credit_line = [0,0,{'account_id' :  self.disburse_journal_id.available_payment_method_ids.ids[1],
                            'partner_id' : self.user_id.partner_id.id,
                            'name' : 'Loan Of ' + name_of,
                            'debit' : self.principal_amount,
                            'credit' : 0.0
                            }]

        move_line = [debit_line,credit_line]

        

        #invoice.action_post()


        jounral = account_move.create({
                    'date': self.applied_date,
                    'journal_id' :self.disburse_journal_id.id,
                    'ref' : str(self.name) ,
                    'line_ids' : move_line})

        jounral.action_post()
        self.write({'state' : 'disbursed','disburse_journal_entry_id':jounral.id,'disbursement_date' : fields.datetime.now()})  # 

        int_debit_line = [0,0,{'account_id' : self.interest_recv_account_id.id,
                            'partner_id' : self.user_id.partner_id.id,
                            'name' : 'Loan Of ' + name_of,
                            'debit' : self.total_interest,
                            'credit' : 0.0
                            }]


        int_credit_line = [0,0,{'account_id' :  self.interest_account_id.id,
                            'partner_id' : self.user_id.partner_id.id,
                            'name' : 'Loan Of ' + name_of,
                            'debit' : 0.0,
                            'credit' : self.total_interest
                            }]

        int_move_line = [int_debit_line,int_credit_line]

        #int_jounral.action_post()
        #self.write({'state' : 'disbursed','account_entery_id':int_jounral.id,'disbursement_date' : fields.datetime.now()}) #
        
        
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
    
