# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'
    

    allow_multiple_loan = fields.Boolean(string="Allow Multiple Loans")
    loan_defaulter = fields.Boolean(string="Loan Defaulter",default=True)
    loan_ids = fields.One2many('loan.request','partner_id')
    policy_ids = fields.Many2many('loan.policies','rel_res_partner_policies_id',string="Partner")
    #balance_on_loan = fields.Float(string="Balance del Prestamo",compute="_compute_balance_on_loan", store=True)    
                

    def get_installment_loan(self,id,date_from,date_to) :
        installment_rec = self.env['loan.installment'].search([('partner_id','=',id),('date_from','=',date_from),
                                                                    ('date_to','=',date_to)],order="id desc", limit=1)
        if installment_rec.pay_from_payroll == True :
            return 0.0
        else :
            return installment_rec.principal_amount

    def get_interest_loan(self,id,date_from,date_to) :
        installment_rec = self.env['loan.installment'].search([('partner_id','=',id),('date_from','=',date_from),
                                                                    ('date_to','=',date_to)],order="id desc", limit=1)
        if installment_rec.pay_from_payroll == True :
            return 0.0
        else :
            return installment_rec.interest_amount

    def button_installment_entries(self):
        return {
            'name': _('Installment Entries'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'loan.request',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.loan_ids.ids)],
        }

    def _compute_balance_on_loan(self) :
        loan_amount = self.env['loan.request'].search([('partner_id','=',id),('state','=','approve')])
        amount = 0


        for line in loan_amount:
            amount = amount + line.balance_on_loan
            self.balance_on_loan = amount




