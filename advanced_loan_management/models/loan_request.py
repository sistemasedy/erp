#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LoanRequest(models.Model):
    """Can create new loan requests and manage records"""
    _name = 'loan.request'
    _inherit = ['mail.thread']
    _description = 'Loan Request'

    name = fields.Char(string='Referencia', readonly=True,
                       copy=False, help="Sequence number for loan requests",
                       default=lambda self: 'New')
    entrada = fields.Boolean(string="Entrada", default=False,
                             help="For monitoring the record")
    salida = fields.Boolean(string="Salida", default=False,
                            help="For monitoring the record")
    company_id = fields.Many2one('res.company', string='Company',
                                 readonly=True,
                                 help="Company Name",
                                 default=lambda self:
                                 self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, help="Currency",
                                  default=lambda self: self.env.user.company_id.
                                  currency_id)

    loan_amount = fields.Float(string="Entrada", store=True,
                               help="Total loan amount", )
    disbursal_amount = fields.Float(string="Balance Pendiente",
                                    help="Total loan amount "
                                         "available to disburse")
    tenure = fields.Integer(string="Tenure",
                            help="Installment period")
    interest_rate = fields.Float(string="Salida", help="Interest "
                                 "percentage")
    date = fields.Date(string="Fecha", default=fields.Date.today(),
                       readonly=True, help="Date")
    partner_id = fields.Many2one('res.partner', string="Cliente",
                                 required=True,
                                 help="Partner")
    repayment_lines_ids = fields.One2many('repayment.line',
                                          'loan_id',
                                          string="Loan Line", index=True,
                                          help="Repayment lines")
    documents_ids = fields.Many2many('loan.documents',
                                     string="Proofs",
                                     help="Documents as proof")
    img_attachment_ids = fields.Many2many('ir.attachment',
                                          relation="m2m_ir_identity_card_rel",
                                          column1="documents_ids",
                                          string="Images",
                                          help="Image proofs")

    reject_reason = fields.Text(string="Reason", help="Displays "
                                                      "rejected reason")
    request = fields.Boolean(string="Request", default=False,
                             help="For monitoring the record")
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                   ('waiting for approval', 'Waiting For Approval'),
                   ('approved', 'Approved'), ('disbursed', 'Disbursed'),
                   ('rejected', 'Rejected'), ('closed', 'Closed')],
        required=True, readonly=True, copy=False,
        tracking=True, default='draft', help="Loan request states")

    @api.model
    def create(self, vals):
        """create  auto sequence for the loan request records"""
        loan_count = self.env['loan.request'].search(
            [('partner_id', '=', vals['partner_id']),
             ('state', 'not in', ('draft', 'rejected', 'closed'))])
        if loan_count:
            for rec in loan_count:
                if rec.state != 'closed':
                    raise UserError(
                        _('The partner has already an ongoing loan.'))
        else:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'increment_loan_ref')
            res = super().create(vals)
            return res

    def action_loan_request(self):
        """Changes the state to confirmed and send confirmation mail"""
        self.write({'state': "confirmed"})
        partner = self.partner_id
        loan_no = self.name
        subject = 'Loan Confirmation'

        message = (f"Dear {partner.name},<br/> This is a confirmation mail "
                   f"for your loan{loan_no}. We have submitted your loan "
                   f"for approval.")

        outgoing_mail = self.company_id.email
        mail_values = {
            'subject': subject,
            'email_from': outgoing_mail,
            'author_id': self.env.user.partner_id.id,
            'email_to': partner.email,
            'body_html': message,
        }
        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()

    def action_loan_complete(self):
        """Changes the state to confirmed and send confirmation mail"""

        self.action_loan_request()
        self.action_compute_repayment()
        self.action_request_for_loan()
        self.action_loan_approved()
        self.action_disburse_loan()

    def action_loan_request(self):
        """Changes the state to confirmed and send confirmation mail"""
        self.write({'state': "confirmed"})
        partner = self.partner_id
        loan_no = self.name
        subject = 'Loan Confirmation'

        message = (f"Dear {partner.name},<br/> This is a confirmation mail "
                   f"for your loan{loan_no}. We have submitted your loan "
                   f"for approval.")

        outgoing_mail = self.company_id.email
        mail_values = {
            'subject': subject,
            'email_from': outgoing_mail,
            'author_id': self.env.user.partner_id.id,
            'email_to': partner.email,
            'body_html': message,
        }
        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()

    def action_request_for_loan(self):
        """Change the state to waiting for approval"""
        if self.request:
            self.write({'state': "waiting for approval"})
        else:
            message_id = self.env['message.popup'].create(
                {'message': _("Compute the repayments before requesting")})
            return {
                'name': _('Repayment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.popup',
                'res_id': message_id.id,
                'target': 'new'
            }

    def action_loan_approved(self):
        """Change to Approved state"""
        self.write({'state': "approved"})

    def action_disburse_loan(self):
        """Disbursing the loan to customer and creating journal
         entry for the disbursement"""
        self.write({'state': "disbursed"})
        return True

    def action_close_loan(self):
        """Closing the loan"""
        demo = []
        for check in self.repayment_lines_ids:
            if check.state == 'unpaid':
                demo.append(check)
        if len(demo) >= 1:
            message_id = self.env['message.popup'].create(
                {'message': _("Pending Repayments")})
            return {
                'name': _('Repayment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.popup',
                'res_id': message_id.id,
                'target': 'new'
            }
        self.write({'state': "closed"})

    def action_loan_rejected(self):
        """You can add reject reasons here"""
        return {'type': 'ir.actions.act_window',
                'name': 'Loan Rejection',
                'res_model': 'reject.reason',
                'target': 'new',
                'view_mode': 'form',
                'context': {'default_loan': self.name}
                }

    def action_compute_repayment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        if self.salida:
            self.action_compute_salida()
        if self.entrada:
            self.action_compute_entrada()

        return True

    def action_compute_salidaaa(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        self.request = True
        for loan in self:
            loan.repayment_lines_ids.unlink()
            date_start = (datetime.strptime(str(loan.date),
                                            '%Y-%m-%d') +
                          relativedelta(months=1))
            entrada = loan.loan_amount
            salida = loan.interest_rate
            balance = loan.disbursal_amount
            partner = self.partner_id

            self.env['repayment.line'].create({
                'name': f"{loan.name}/{self.repayment_lines_ids.id}",
                'partner_id': partner.id,
                'date': self.date,
                'amount': entrada,
                'interest_amount': salida,
                'total_amount': balance,
                'loan_id': loan.id})

        return True

    def action_compute_entradaaa(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        self.request = True
        for loan in self:
            loan.repayment_lines_ids.unlink()
            date_start = (datetime.strptime(str(loan.date),
                                            '%Y-%m-%d') +
                          relativedelta(months=1))
            entrada = loan.loan_amount
            salida = loan.interest_rate
            balance = loan.disbursal_amount
            partner = self.partner_id

            self.env['repayment.line'].create({
                'name': f"{loan.name}/{self.repayment_lines_ids.id}",
                'partner_id': partner.id,
                'date': self.date,
                'amount': entrada,
                'interest_amount': salida,
                'total_amount': balance,
                'loan_id': loan.id})

        return True

    @api.multi
    def action_compute_salida(self):
        self.ensure_one()
        repayment_line_vals = {
            'loan_id': self.id,
            'name': f"{loan.name}/{self.repayment_lines_ids.id}",
            'partner_id': partner.id,
            'date': self.date,
            'amount': entrada,
            'interest_amount': salida,
            'total_amount': balance,
        }
        self.env['repayment.line'].create(repayment_line_vals)
        return True

    @api.multi
    def action_compute_entrada(self):
        self.ensure_one()
        repayment_line_vals = {
            'loan_id': self.id,
            'name': f"{loan.name}/{self.repayment_lines_ids.id}",
            'partner_id': partner.id,
            'date': self.date,
            'amount': entrada,
            'interest_amount': salida,
            'total_amount': balance,
        }
        self.env['repayment.line'].create(repayment_line_vals)
        return True
