from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError


class CustomerDeposit(models.Model):
    _name = 'customer.deposit'
    _description = 'Depósitos de Clientes'

    name = fields.Char(string="Referencia", required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))
    
