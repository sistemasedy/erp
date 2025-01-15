from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CustomerDeposit(models.Model):
    _name = 'customer.deposit'
    _description = 'Depósitos de Clientes'

    name = fields.Char(string="Referencia", required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    deposit_date = fields.Date(string="Fecha del Depósito", default=fields.Date.today, required=True)
    amount = fields.Monetary(string="Monto", required=True)
    currency_id = fields.Many2one('res.currency', string="Moneda", required=True, default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado')
    ], string="Estado", default='draft', required=True)
    remaining_amount = fields.Monetary(string="Monto Restante", compute="_compute_remaining_amount", store=True)

    @api.depends('amount', 'state')
    def _compute_remaining_amount(self):
        for record in self:
            if record.state == 'confirmed':
                applied_amount = sum(self.env['account.move.line'].search([
                    ('deposit_id', '=', record.id),
                    ('move_id.state', '=', 'posted')
                ]).mapped('debit'))
                record.remaining_amount = record.amount - applied_amount
            else:
                record.remaining_amount = record.amount

    @api.model
    def create(self, vals):
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('customer.deposit') or _('Nuevo')
        return super(CustomerDeposit, self).create(vals)

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_register_deposit(self):
        return {
            'name': _('Registrar Depósito'),
            'type': 'ir.actions.act_window',
            'res_model': 'customer.deposit',
            'view_mode': 'form',
            'view_id': False,
            'context': {
                'default_partner_id': self.id,
            },
            'target': 'new',
        }

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    deposit_id = fields.Many2one('customer.deposit', string="Depósito Aplicado")

class AccountMove(models.Model):
    _inherit = 'account.move'

    deposit_ids = fields.Many2many('customer.deposit', string="Depósitos Aplicados")

    def action_apply_deposit(self):
        for invoice in self:
            available_deposits = self.env['customer.deposit'].search([
                ('partner_id', '=', invoice.partner_id.id),
                ('remaining_amount', '>', 0),
                ('state', '=', 'confirmed')
            ])

            for deposit in available_deposits:
                if invoice.amount_residual <= 0:
                    break

                to_apply = min(deposit.remaining_amount, invoice.amount_residual)

                self.env['account.move.line'].create({
                    'move_id': invoice.id,
                    'name': _('Aplicación de Depósito: %s') % deposit.name,
                    'partner_id': invoice.partner_id.id,
                    'account_id': invoice.journal_id.default_account_id.id,
                    'debit': 0.0,
                    'credit': to_apply,
                    'currency_id': deposit.currency_id.id,
                    'deposit_id': deposit.id
                })

                invoice.amount_residual -= to_apply
