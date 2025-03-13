import re
from psycopg2 import sql
from werkzeug import urls

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError


class AccountMove(models.Model):
    _inherit = "account.move"

    # Journal
    fiscal_ref = fields.Char(string='Comprobante')
    partner_vat = fields.Char(related='partner_id.vat', string='RNC')
    partner_phone = fields.Char(
        related='partner_id.phone', string='Teléfono del cliente')
    partner_email = fields.Char(
        related='partner_id.email', string='Email del cliente')
    validates_journal = fields.Boolean(help="Activa para comfirmar")

    validate_journal = fields.Selection(selection=[
        ('entry', 'Recuelda Selecional el Diario'),
        ('out_invoice', 'Recuelda Selecional'),
    ], string='Type', store=True, index=True)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    quantity = fields.Float(digits=(2, 2))

    monto = fields.Float(
        string='Monto',  compute='_compute_monto', digits=(2, 2), store=True)
    itbis = fields.Float(
        string='Itbis',  compute='_compute_itbis', digits=(2, 2), store=True)

    @api.depends('price_unit', 'quantity')
    def _compute_monto(self):
        for r in self:
            r.monto = ((r.price_unit*r.quantity))
            # r.monto = ((r.price_unit*r.quantity)+(r.price_subtotal*.18))
            # r.monto = ((r.price_subtotal*.18)+(r.price_subtotal))

    @api.depends('price_unit', 'quantity')
    def _compute_itbis(self):
        for r in self:
            # r.itbis = ((r.price_subtotal- r.monto))
            # r.itbis = ((r.price_subtotal*((r.tax_ids.amount)/100)))
            r.itbis = ((r.price_subtotal * ((r.tax_ids[:1].amount) / 100)))

    # @api.depends('price_unit', 'quantity')
    # def _compute_total(self):
    #    for r in self:
    #        r.total = r.price_subtotal+r.itbi

    # @api.depends('price_unit', 'quantity')
    # def _compute_itbi(self):
    #    for r in self:
     #       r.itbi = ((r.price_subtotal*.18))


class cotizacion(models.Model):
    _inherit = 'sale.order.line'

    monto = fields.Float(
        string='Monto',  compute='_compute_monto', digits=(2, 2), store=True)
    itbis = fields.Float(
        string='Itbis',  compute='_compute_itbis', digits=(2, 2), store=True)

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_monto(self):
        for r in self:
            r.monto = ((r.price_unit*r.product_uom_qty))

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_itbis(self):
        for r in self:
            # r.itbis = ((r.price_subtotal*((r.tax_id.amount)/100)))
            r.itbis = ((r.price_subtotal * ((r.tax_ids[:1].amount) / 100)))
