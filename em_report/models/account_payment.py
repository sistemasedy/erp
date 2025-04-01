# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime,date, timedelta
from dateutil.relativedelta import relativedelta
import base64


class account_move(models.Model):
    
    _inherit = 'account.move'
    _order = 'invoice_date_due'
    
    

    abono_amount = fields.Float(string="Tiene Abono A su Favor")
    abono = fields.Float(string="Balance a Pagar") #'balance' field is not the sames
    allow_abono = fields.Boolean(string="Activo")
    afavor_abono = fields.Boolean(string="Activo")

    @api.onchange('partner_id')
    def _onchange_overdue_abono(self):
        for aml in self:
            if self.partner_id.allow_multiple_loan:
                aml.abono_amount = 0.0
                aml.abono_amount = self.partner_id.payment_amount_loan_amt
            if self.partner_id.allow_multiple_loan:
                self.afavor_abono = True

    def action_post(self):
        """Change repayment record state to 'invoiced'
        while reset to draft the invoice"""
        res = super().action_post()
        loan_line_ids = self.env['loan.request'].search([('partner_id','=',self.partner_id.id),('state','=','approved')])
        if self.partner_id.allow_multiple_loan:
            if self.partner_id.payment_amount_loan_amt != 0.0:
                self.abono = abs(self.amount_residual) - abs(self.partner_id.payment_amount_loan_amt)
                self.action_compute_abono()
                self.allow_abono = True
            
            
        return res

    def action_compute_abono(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        amount_due = amount_overdue = 0.0
        if self.partner_id.payment_amount_loan_amt > self.amount_residual or self.partner_id.payment_amount_loan_amt == self.amount_residual:
            amount_due = self.amount_residual
        if self.partner_id.payment_amount_loan_amt < self.amount_residual and self.partner_id.payment_amount_loan_amt != 0.0:
            amount_due = self.partner_id.payment_amount_loan_amt
        loan_line_ids = self.env['loan.request'].search([('partner_id','=',self.partner_id.id),('state','=','approved')])
        for loan in self:
            partner = self.partner_id
            self.env['loan.request'].create({
                'partner_id': partner.id,
                'principal_amount': 0.0,
                'salida': amount_due,
                'ref_invoice': self.name,
                'ref_loan': loan_line_ids.name})

                
        return True
