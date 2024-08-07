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
    start_date = fields.Date(string='Fecha de Inicio', default=lambda self: fields.Date.today() - timedelta(days=30))
    end_date = fields.Date(string='Fecha de Fin', default=fields.Date.today)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    #order_line = fields.One2many('report.sale.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    
    state = fields.Selection([('unpaid','Pendiente'),('approve','Aprovado'),('paid','Pagado')],default='unpaid',string="Estado")
    

    installment_number = fields.Integer(string="Renglon")
    date_from = fields.Date(string="Date From")
    date_to  = fields.Date(string="Date To")
    opening_balance_amount = fields.Float(string="Balance",digits=(16, 2))
    ending_balance_amount = fields.Float(string="Balance",digits=(16, 2))
    
    interest_amount = fields.Float(string="Interes",digits=(32, 2))
    emi_installment = fields.Float(string="A Pagar",digits=(32, 2))
    
    
    loan_id = fields.Many2one('loan.request',string="Ref")
    loan_type_id = fields.Many2one('loan.type',string="Tipo")
    
    interest_acouunting_id = fields.Many2one('account.move',string="Interest Accounting Entry",readonly=True)
    accounting_entry_id = fields.Many2one('account.move',string="Accounting Entry",readonly=True)
    pay_from_payroll = fields.Boolean(string="Payroll")
    installment_booked = fields.Boolean(string="Payroll")
    loan_partner_type = fields.Selection([('customer','Customer'),('vendor','Supplier')],string="Loan Partner Type")

    date = fields.Date(string="Fecha", required=True,
                       default=fields.Date.today(),
                       help="Date of the payment")

    capital_total = fields.Boolean(string="Pago Total", default=False,
                                   help="For monitoring the record")

    partial = fields.Boolean(string="Pago parcial de Interes", default=False,
                             help="For monitoring the record")
    partial_amount = fields.Float(string="Pago de Capital", help="Amount",
                                  digits=(16, 2))
    partial_interes = fields.Float(string="Pago de Interes", help="Amount",
                                   digits=(16, 2))

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

    bal_pendiente = fields.Float(string="Balance Pendiente", help="Amount",
                                 digits=(16, 2))


    overdue_interest_rate = fields.Float(
        string="Overdue Interest Rate (%)", default=0.05)
    overdue_days = fields.Integer(
        string="Overdue Days", compute='_compute_overdue_days')
    overdue_amount = fields.Float(
        string="Mora", compute='_compute_overdue_amount')

    overdue_days1 = fields.Integer(
        string="Overdue Days", compute='_compute_overdue_days')

    @api.depends('date_to', 'state')
    def _compute_overdue_days(self):
        #class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        for invoice in self:
            if invoice.state != 'paid' and invoice.date:  # corection no close, is paid
                today = fields.Date.today()
                overdue_days = (today - invoice.date).days
                #overdue_days1 = (today - invoice.date).minutes
                #invoice.overdue_days1 = overdue_days1 if overdue_days > 0 else 0
                invoice.overdue_days = overdue_days if overdue_days > 0 else 0
            else:
                invoice.overdue_days = 0

    @api.depends('overdue_days', 'overdue_interest_rate', 'ending_balance_amount')
    def _compute_overdue_amount(self):
        self.overdue_interest_rate = self.loan_id.loan_type_id.taza_mora
        for invoice in self:
            #invoice.overdue_amount = ((invoice.principal_amount + invoice.interest_amount) * invoice.overdue_interest_rate * invoice.overdue_days) / 100
            if invoice.loan_id.interest_mode == "reducing":
                invoice.overdue_amount = ((invoice.principal_amount + invoice.interest_amount) * invoice.overdue_interest_rate * invoice.overdue_days) / 100
            else:
                invoice.overdue_amount = ((invoice.interest_amount) * invoice.overdue_interest_rate * invoice.overdue_days) / 100
            invoice.ending_balance_amount = invoice.principal_amount + invoice.interest_amount + invoice.overdue_amount

    @api.onchange('date_to', 'state')
    def _onchange_overdue_fields(self):
        for invoice in self:
            invoice._compute_overdue_days()
            invoice._compute_overdue_amount()

    @api.depends('installment_number','loan_id')
    def _compute_name(self):
        for line in self :
            if line.loan_id and line.installment_number :
                line.name = line.loan_id.name + '/' + str(line.installment_number)
        return

    def approve_payment(self):
        self.write({'state':'approve'})



    @api.onchange('partial_amount','partial_interes')
    def _compute_pay_partial(self):
        rate = self.loan_id.loan_type_id.rate/100

        for line in self :
            total_paid = 0.0
            total_inte = 0.0
            if self.loan_id.interest_mode != "reducing":
                if line.partial_amount > 0:
                    line.principal_amount = line.partial_amount
                if line.partial_interes > 0:
                    line.interest_amount = line.partial_interes
                
                total_paid = total_paid + line.partial_amount
                line.sum_paid = line.sum_paid + total_paid

                total_inte = total_inte + ((line.principal_amount * rate) -line.partial_interes)

                line.sum_int_pendiente = line.sum_int_pendiente + total_inte

            
        return

    


    @api.onchange('date_to')
    def _onchange_overdue_automate(self):
        for invoice in self:
            invoice._compute_create_invoiceds()





    def action_payment(self):
        #if self.invoice_image:
        rate = self.loan_id.loan_type_id.rate/100
        time_now = self.date
        account_move = self.env['account.move']
        
        name_of = self.partner_id.name

        interest_product_id = self.env['ir.config_parameter'].sudo().get_param(
            'odoo_customer_supplier_loan_app.interest_product_id')
        repayment_product_id = self.env['ir.config_parameter'].sudo().get_param(
            'odoo_customer_supplier_loan_app.repayment_product_id')
        mora_product_id = self.env['ir.config_parameter'].sudo().get_param(
            'odoo_customer_supplier_loan_app.mora_product_id')


        if self.loan_id.interest_mode == "reducing":
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'invoice_date': fields.datetime.now(),
                'partner_id': self.partner_id.id,
                'payment_reference': self.name,
                'capital_monto': self.principal_amount,
                'interes_monto': self.interest_amount,
                'mora_monto': self.overdue_amount,
                'total_monto': self.emi_installment,
                'invoiced_image': self.loan_type_id.invoice_image,
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': repayment_product_id,
                        'price_unit': self.principal_amount,
                        'name': 'CUOTA',
                        'account_id': self.loan_id.interest_recv_account_id.id,
                        'quantity': 1,
                    }),
                    (0, 0, {
                        'price_unit': self.interest_amount,
                        'product_id': interest_product_id,
                        'name': 'INTERESES',
                        'quantity': 1,
                    }),
                    (0, 0, {
                        'product_id': mora_product_id,
                        'price_unit': self.overdue_amount,
                        'name': 'MORA',
                        'account_id': self.loan_id.interest_account_id.id,
                        'quantity': 1,
                    }),
                ],
            })
            # Validar la factura recién creada
            #invoice.sudo().action_post()

            self.installment_booked = True
            self.write({'accounting_entry_id' :invoice.id,'state':'paid' })
            #self.action_pay_emi()
        elif self.loan_id.interest_mode == "float" and self.partial_amount == 0:

            if self.loan_id.loan_type_id.tenure_plan == 'week':
                date_start = (datetime.strptime(str(time_now),'%Y-%m-%d') + relativedelta(weeks=1))
                date_start += relativedelta(weeks=1)
                self.date = date_start
                self.mora = 29
            if self.loan_id.loan_type_id.tenure_plan == 'fortnight':
                date_start = (datetime.strptime(str(time_now),
                                                '%Y-%m-%d') +
                              relativedelta(days=15))
                date_start += relativedelta(days=15)
                self.date = date_start
            if self.loan_id.loan_type_id.tenure_plan == 'monthly':
                date_start = (datetime.strptime(str(time_now),
                                                '%Y-%m-%d') +
                              relativedelta(months=1))
                date_start += relativedelta(months=1)
                self.date = date_start


            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'invoice_date': fields.datetime.now(),
                'partner_id': self.partner_id.id,
                'payment_reference': self.name,
                'capital_monto': self.principal_amount,
                'interes_monto': self.interest_amount,
                'mora_monto': self.overdue_amount,
                'total_monto': self.emi_installment,
                'invoiced_image': self.loan_type_id.invoice_image,
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': repayment_product_id,
                        'price_unit': 0.0,
                        'name': 'CUOTA',
                        'account_id': self.loan_id.interest_recv_account_id.id,
                        'quantity': 1,
                    }),
                    (0, 0, {
                        'price_unit': self.interest_amount,
                        'product_id': interest_product_id,
                        'name': 'INTERESES',
                        'quantity': 1,
                    }),
                    (0, 0, {
                        'product_id': mora_product_id,
                        'price_unit': self.overdue_amount,
                        'name': 'MORA',
                        'account_id': self.loan_id.interest_account_id.id,
                        'quantity': 1,
                    }),
                ],
            })
            # Validar la factura recién creada
            #invoice.sudo().action_post()

            self.installment_booked = True
        

        else:
            if self.loan_id.loan_type_id.tenure_plan == 'week':
                date_start = (datetime.strptime(str(time_now),'%Y-%m-%d') + relativedelta(weeks=1))
                date_start += relativedelta(weeks=1)
                self.date = date_start
                self.mora = 29
            if self.loan_id.loan_type_id.tenure_plan == 'fortnight':
                date_start = (datetime.strptime(str(time_now),
                                                '%Y-%m-%d') +
                              relativedelta(days=15))
                date_start += relativedelta(days=15)
                self.date = date_start
            if self.loan_id.loan_type_id.tenure_plan == 'monthly':
                date_start = (datetime.strptime(str(time_now),
                                                '%Y-%m-%d') +
                              relativedelta(months=1))
                date_start += relativedelta(months=1)
                self.date = date_start
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'invoice_date': fields.datetime.now(),
                'partner_id': self.partner_id.id,
                'payment_reference': self.name,
                'capital_monto': self.principal_amount,
                'interes_monto': self.interest_amount,
                'mora_monto': self.overdue_amount,
                'total_monto': self.emi_installment,
                'invoiced_image': self.loan_type_id.invoice_image,
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': repayment_product_id,
                        'price_unit': self.partial_amount,
                        'name': 'CUOTA',
                        'account_id': self.loan_id.interest_recv_account_id.id,
                        'quantity': 1,
                    }),
                    (0, 0, {
                        'price_unit': self.interest_amount,
                        'product_id': interest_product_id,
                        'name': 'INTERESES',
                        'quantity': 1,
                    }),
                    (0, 0, {
                        'product_id': mora_product_id,
                        'price_unit': self.overdue_amount,
                        'name': 'MORA',
                        'account_id': self.loan_id.interest_account_id.id,
                        'quantity': 1,
                    }),
                ],
            })
            

            self.installment_booked = True




        if self.loan_id.interest_mode != "reducing":
            if self.partial_amount>0:
                self.principal_amount = self.loan_id.principal_amount - self.sum_paid
                self.interest_amount = self.principal_amount * rate


            if self.partial_interes>0:
                self.interest_amount = (self.principal_amount * rate) + self.sum_int_pendiente
                if self.partial:
                    #self.sum_int_pendiente = self.suma_inte - self.partial_interes
                    self.interest_amount = (self.principal_amount * rate) + self.sum_int_pendiente
                    self.partial = False
                self.principal_amount = self.loan_id.principal_amount - self.sum_paid
                #self.interest_amount = self.principal_amount * rate


            if self.partial_interes == 0 and self.sum_int_pendiente == 0:
                self.interest_amount = (self.principal_amount * rate)
                self.suma_inte = 0
                self.sum_parcial = 0
                # self.mora = 5
                self.partial = True


            if self.partial_interes == 0 and self.sum_int_pendiente > 0:
                self.interest_amount = (self.principal_amount * rate)
                self.sum_int_pendiente = 0
                self.suma_inte = 0
                self.sum_parcial = 0
                
                self.partial = True
                

            self.partial_amount = 0
            self.partial_interes = 0


        self.emi_installment = self.principal_amount + self.interest_amount + self.overdue_amount
        #self.action_close_loan()
        if self.loan_id.balance_on_loan == 0:
            self.loan_id.write({'state': 'closed'})
        # Validar la factura recién creada
        invoice.sudo().action_post()
        if self.loan_type_id.invoice_image:
            invoice.sudo().download_invoice_preview()
        

        return {
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }




    def action_close_loan(self):
        """Closing the loan"""
        demo = []
        installment_ids = self.env['loan.installment'].search([('loan_id','=',self.loan_id.id)])
        for check in installment_ids:
            if check.state == 'unpaid' or 'approve':
                demo.append(check)
        if len(demo) >= 1:
            self.loan_id.write({'state': 'approve'})
        else:
            self.loan_id.write({'state': 'closed'})


   

    def reset_draft(self):
        self.write({'state':'unpaid'})

   
    def book_interest(self):
        pass


