# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseFiscalReport(models.Model):
    _name = 'purchase.fiscal.report'
    _inherit = 'purchase.order' # purchase.order, NOT sale.order

    ncf_tax = fields.Monetary(string='Impuesto NCF',
                               currency_field='currency_id',
                               readonly=False,
                               store=True,
                               compute='_compute_ncf_amounts',
                               help="Impuesto calculado para el NCF.")

    ncf_year_month = fields.Char(string='Año/Mes NCF', help="Año y mes de la transacción para el NCF.")