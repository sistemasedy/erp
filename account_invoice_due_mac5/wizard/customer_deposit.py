from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomerDeposit(models.Model):
    _name = 'customer.deposit'
    _description = 'Depósitos de Clientes'

    name = fields.Char(string="Referencia", required=True,
                       copy=False, readonly=True, default=lambda self: _('Nuevo'))
    partner_id = fields.Many2one(
        'res.partner', string="Cliente", required=True)
    deposit_date = fields.Date(
        string="Fecha del Depósito", default=fields.Date.today, required=True)
    amount = fields.Monetary(string="Monto", required=True)
    currency_id = fields.Many2one('res.currency', string="Moneda",
                                  required=True, default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('applied', 'Aplicado'),
        ('applied_parcial', 'Aplicado Parcial')
    ], string="Estado", default='draft', required=True)
    remaining_amount = fields.Monetary(
        string="Monto Restante", compute="_compute_remaining_amount", store=True)
    journal_id = fields.Many2one('account.journal', string="Diario", required=True,
                                 default=lambda self: self.env['account.journal'].search([('type', '=', 'cash')], limit=1))
    liquidity_account_id = fields.Many2one('account.account', string="Cuenta de Liquidez", required=True,
                                           default=lambda self: self.env['account.account'].search([('user_type_id.type', '=', 'liquidity')], limit=1))

    @api.depends('amount', 'state')
    def _compute_remaining_amount(self):
        for record in self:
            if record.state == 'applied_parcial':
                applied_amount = sum(self.env['account.move.line'].search([
                    ('deposit_id', '=', record.id),
                    ('move_id.state', '=', 'posted')
                ]).mapped('debit'))
                record.remaining_amount = record.amount - applied_amount

            if record.state == 'applied':
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
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'customer.deposit') or _('Nuevo')
        return super(CustomerDeposit, self).create(vals)

    def action_confirm(self):
        for record in self:
            if record.state != 'confirmed':
                record.state = 'confirmed'
                # Crear asiento contable para el depósito
                record._create_account_move()

    def _create_account_move(self):
        self.ensure_one()
        move_vals = {
            'journal_id': self.journal_id.id,
            'date': self.deposit_date,
            'ref': _('Depósito confirmado: %s') % self.name,
            'line_ids': [
                # Línea de débito (cuenta por cobrar del cliente)
                (0, 0, {
                    'account_id': self.partner_id.property_account_receivable_id.id,
                    'partner_id': self.partner_id.id,
                    'name': _('Dep conf: %s (%s)') % (self.name, self.deposit_date),
                    'debit': 0.0,
                    'credit': self.amount,
                    'currency_id': self.currency_id.id,
                }),
                # Línea de crédito (cuenta de liquidez)
                (0, 0, {
                    'account_id': self.liquidity_account_id.id,
                    'partner_id': self.partner_id.id,
                    'name': _('Dep conf: %s (%s)') % (self.name, self.deposit_date),
                    'debit': self.amount,
                    'credit': 0.0,
                    'currency_id': self.currency_id.id,
                }),
            ],
        }
        move = self.env['account.move'].create(move_vals)
        move.action_post()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # days_limit = fields.Char(string='Dias de Vencimiento')
    deposit_ids = fields.One2many('customer.deposit', 'partner_id', 'Deposits', compute='_compute_deposits') # Added field
    #... other fields...

    @api.depends('id')  # Trigger recomputation when the partner changes
    def _compute_deposits(self):
        for partner in self:
            partner.deposit_ids = self.env['customer.deposit'].search([('partner_id', '=', partner.id)])

    def action_register_deposit(self):
        return {
            'name': _('Registrar Depósito'),
            'type': 'ir.actions.act_window',
            'res_model': 'customer.deposit',
            'view_mode': 'form',
            'context': {'default_partner_id': self.id},
            'target': 'new',
        }


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    deposit_id = fields.Many2one(
        'customer.deposit', string="Depósito Aplicado")


class AccountMove(models.Model):
    _inherit = 'account.move'

    deposit_ids = fields.Many2many(
        'customer.deposit', string='Depósitos',
        domain="[('partner_id', '=', partner_id), ('remaining_amount', '>', 0), ('state', '=', 'confirmed')]"
    )
    applied_balance = fields.Monetary(
        string='Monto Aplicado', compute='_compute_applied_balance', store=True
    )
    remaining_balance = fields.Monetary(
        string='Saldo Pendiente Final', compute='_compute_remaining_balance', store=True
    )

    @api.depends('deposit_ids', 'deposit_ids.remaining_amount')
    def _compute_applied_balance(self):
        """Calcula el monto total de los depósitos seleccionados"""
        for move in self:
            move.applied_balance = sum(
                deposit.remaining_amount for deposit in move.deposit_ids)

    @api.depends('amount_residual', 'applied_balance')
    def _compute_remaining_balance(self):
        """Calcula el saldo pendiente de la factura después de aplicar depósitos"""
        for move in self:
            move.remaining_balance = move.amount_residual - move.applied_balance

    def action_open_apply_deposit_form(self):
        """Muestra el formulario para aplicar depósitos."""
        self.ensure_one()
        deposits = self.env['customer.deposit'].search([
            ('partner_id', '=', self.partner_id.id),
            ('remaining_amount', '>', 0),
            ('state', '=', 'confirmed')
        ])
        if not deposits:
            raise UserError(_('No hay depósitos disponibles para aplicar.'))

        return {
            'name': _('Aplicar Depósitos'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.id,
            'view_id': self.env.ref('account_invoice_due_mac5.view_apply_deposit_form').id,
            'target': 'new',
            'context': {
                'default_partner_id': self.partner_id.id,
            }
        }

    def action_confirm_apply_deposit(self):
        """Aplica los depósitos seleccionados a la factura."""
        self.ensure_one()

        # Validar si existen depósitos seleccionados
        if not self.deposit_ids:
            raise UserError(
                _('No se han seleccionado depósitos para aplicar.'))

        move_lines = []
        for deposit in self.deposit_ids:
            if self.amount_residual <= 0:
                break

            # Calcular cuánto se aplicará del depósito (mínimo entre el depósito y el saldo pendiente)
            to_apply = min(deposit.remaining_amount, self.amount_residual)

            # Crear las líneas contables para reflejar el uso del depósito
            move_lines.extend([
                # Línea de débito (aplicación del depósito al cliente)
                (0, 0, {
                    'partner_id': self.partner_id.id,
                    'account_id': self.partner_id.property_account_receivable_id.id,
                    'name': _('Aplicación de Depósito: %s') % deposit.name,
                    'debit': to_apply,
                    'credit': 0.0,
                    'currency_id': deposit.currency_id.id,
                    'deposit_id': deposit.id,
                }),
                # Línea de crédito (reducción del depósito)
                (0, 0, {
                    'partner_id': self.partner_id.id,
                    'account_id': self.journal_id.default_account_id.id,
                    'name': _('Contrapartida Depósito: %s') % deposit.name,
                    'debit': 0.0,
                    'credit': to_apply,
                    'currency_id': deposit.currency_id.id,
                    'deposit_id': deposit.id,
                }),
            ])

            # Actualizar los montos residuales
            self.amount_residual -= to_apply
            deposit.remaining_amount -= to_apply
            deposit.write({'remaining_amount': deposit.remaining_amount})

         # Actualizar el estado del depósito a 'applied' si se ha usado completamente
        if deposit.remaining_amount == 0:
            deposit.write({'state': 'applied'})
        else:
            deposit.write({'state': 'applied_parcial'})

        # Crear y publicar el asiento contable
        if move_lines:
            move = self.env['account.move'].create({
                'journal_id': self.journal_id.id,
                'date': fields.Date.today(),
                'ref': _('Aplicación de Depósitos para Factura: %s') % self.name,
                'line_ids': move_lines,
            })
            move.action_post()

        # Actualizar la factura como pagada si el saldo pendiente llega a 0
        if self.amount_residual == 0:
            self.payment_state = 'paid'


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    deposit_id = fields.Many2one(
        'customer.deposit', string="Depósito Aplicado")
