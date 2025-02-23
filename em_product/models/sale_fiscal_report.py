# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseFiscalReport(models.Model):
    _name = 'purchase.fiscal.report'
    _inherit = 'purchase.order' # purchase.order, NOT sale.order

    ncf_year_month = fields.Char(string='Año/Mes NCF', help="Año y mes de la transacción para el NCF.")