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
    journal_id = fields.Many2one('account.journal', string="Diario", required=True, 
                                 default=lambda self: self.env['account.journal'].search([('type', '=', 'cash')], limit=1))
    liquidity_account_id = fields.Many2one('account.account', string="Cuenta de Liquidez", required=True, 
                                           default=lambda self: self.env['account.account'].search([('user_type_id.type', '=', 'liquidity')], limit=1))

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
        deposit = super(CustomerDeposit, self).create(vals)
        # Actualizar balance positivo del cliente
        if deposit.state == 'confirmed':
            deposit._update_partner_balance(deposit.amount)
        return deposit

    def action_confirm(self):
        for record in self:
            if record.state != 'confirmed':
                record.state = 'confirmed'
                # Actualizar balance positivo del cliente
                record._update_partner_balance(record.amount)

    def _update_partner_balance(self, amount):
        self.ensure_one()
        move_env = self.env['account.move']
        move_line_env = self.env['account.move.line']

        move = move_env.create({
            'partner_id': self.partner_id.id,
            'journal_id': self.journal_id.id,
            'date': self.deposit_date,
            'ref': _('Depósito confirmado: %s') % self.name,
            'line_ids': []
        })

        # Crear las líneas contables asociadas al asiento
        debit_line = move_line_env.create({
            'move_id': move.id,
            'partner_id': self.partner_id.id,
            'account_id': self.partner_id.property_account_receivable_id.id,
            'debit': amount,
            'credit': 0.0,
            'name': _('Depósito confirmado: %s') % self.name,
        })
        credit_line = move_line_env.create({
            'move_id': move.id,
            'partner_id': self.partner_id.id,
            'account_id': self.liquidity_account_id.id,
            'debit': 0.0,
            'credit': amount,
            'name': _('Depósito confirmado: %s') % self.name,
        })

        # Asegurarse de que las líneas contables estén balanceadas
        if debit_line.debit != credit_line.credit:
            raise UserError(_('El asiento de diario no está balanceado. '
                            'Débito: %s, Crédito: %s,Mont: %s') % (debit_line.debit, credit_line.credit, amount))


        # Publicar el asiento de diario
        move.action_post()

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
                    break  # Si la factura ya está cubierta, salir del bucle.

                # Determinar cuánto aplicar del depósito (lo menor entre el saldo del depósito y el residual de la factura).
                to_apply = min(deposit.remaining_amount, invoice.amount_residual)

                # Crear la línea de crédito (aplicación del depósito).
                self.env['account.move.line'].create({
                    'move_id': invoice.id,
                    'name': _('Aplicación de Depósito: %s') % deposit.name,
                    'partner_id': invoice.partner_id.id,
                    'account_id': invoice.journal_id.default_account_id.id,  # Cuenta predeterminada del diario.
                    'debit': 0.0,
                    'credit': to_apply,
                    'currency_id': deposit.currency_id.id,
                    'deposit_id': deposit.id
                })

                # Crear la contrapartida de débito.
                self.env['account.move.line'].create({
                    'move_id': invoice.id,
                    'name': _('Contrapartida Depósito: %s') % deposit.name,
                    'partner_id': invoice.partner_id.id,
                    'account_id': deposit.partner_id.property_account_receivable_id.id,  # Cuenta por cobrar del cliente.
                    'debit': to_apply,
                    'credit': 0.0,
                    'currency_id': deposit.currency_id.id,
                    'deposit_id': deposit.id
                })

                # Reducir el residual de la factura y actualizar el balance restante del depósito.
                invoice.amount_residual -= to_apply
                deposit.remaining_amount -= to_apply

                # Registrar el cambio en el depósito.
                deposit.write({'remaining_amount': deposit.remaining_amount})
