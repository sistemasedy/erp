from odoo import fields, models, _
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

    @api.model
    def create(self, vals):
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('customer.deposit') or _('Nuevo')
        return super(CustomerDeposit, self).create(vals)

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
