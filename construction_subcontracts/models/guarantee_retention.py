# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ConstructionGuaranteeRetention(models.Model):
    _name = 'construction.guarantee.retention'
    _description = 'Garantía Retenida de Subcontrato'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_release desc'

    name = fields.Char(
        string='Referencia',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nueva')
    )

    subcontract_id = fields.Many2one(
        comodel_name='construction.subcontract',
        string='Subcontrato',
        required=True,
        ondelete='cascade'
    )

    partner_id = fields.Many2one(
        related='subcontract_id.partner_id',
        string='Ajustero',
        store=True
    )

    amount_retained = fields.Monetary(
        string='Monto Retenido',
        required=True,
        currency_field='currency_id'
    )

    date_retention = fields.Date(
        string='Fecha de Retención',
        required=True,
        default=fields.Date.context_today
    )

    date_release = fields.Date(
        string='Fecha de Liberación',
        tracking=True
    )

    state = fields.Selection(
        selection=[
            ('retained', 'Retenido'),
            ('released', 'Liberado'),
            ('cancelled', 'Cancelado'),
        ],
        string='Estado',
        default='retained',
        required=True,
        tracking=True
    )

    release_invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='Factura de Liberación',
        readonly=True
    )

    notes = fields.Text(string='Notas')

    currency_id = fields.Many2one(
        related='subcontract_id.currency_id'
    )

    company_id = fields.Many2one(
        related='subcontract_id.company_id',
        store=True
    )

    @api.model
    def create(self, vals):
        if vals.get('name', _('Nueva')) == _('Nueva'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.guarantee.retention'
            ) or _('Nueva')
        return super().create(vals)

    def action_release(self):
        """Liberar garantía y generar factura de pago"""
        self.ensure_one()
        if self.state != 'retained':
            raise ValidationError(
                _('Solo se pueden liberar garantías en estado "Retenido".')
            )

        # Crear factura de liberación
        invoice = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [(0, 0, {
                'name': f'Liberación Garantía - {self.subcontract_id.name}',
                'quantity': 1,
                'price_unit': self.amount_retained,
            })],
        })

        self.write({
            'state': 'released',
            'date_release': fields.Date.context_today(self),
            'release_invoice_id': invoice.id,
        })

        self.message_post(
            body=_('Garantía liberada. Factura creada: %s') % invoice.name
        )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
