# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseFiscalReport(models.Model):
    _name = 'purchase.fiscal.report'
    _inherit = 'purchase.order' # purchase.order, NOT sale.order

    
                                 currency_field='currency_id',
                                 readonly=True,
                                 store=True,
                                 compute='_compute_ncf_total',
                                 help="Total de la venta para el NCF (con impuesto).")
    ncf_day = fields.Char(string='Día NCF', help="Día de la transacción para el NCF.")
    
        self._compute_ncf_amounts()