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

    ncf_amount_purchase = fields.Monetary(string='Monto de Venta NCF',
                                        currency_field='currency_id',
                                        readonly=False,
                                        store=True,
                                        compute='_compute_ncf_amounts',
                                        help="Monto de la venta para el NCF (sin impuesto).")
    ncf_total = fields.Monetary(string='Total NCF',
                                 currency_field='currency_id',
                                 readonly=True,
                                 store=True,
                                 compute='_compute_ncf_total',
                                 help="Total de la venta para el NCF (con impuesto).")
    ncf_day = fields.Char(string='Día NCF', help="Día de la transacción para el NCF.")
    ncf_year_month = fields.Char(string='Año/Mes NCF', help="Año y mes de la transacción para el NCF.")
    ncf_check = fields.Boolean(string='Verificación NCF', help="Indica si el NCF ha sido verificado.")

    check_complete = fields.Boolean(string='Completado', help="Indica si el registro está completo.")
    check_verificate = fields.Boolean(string='Verificado', help="Indica si el registro ha sido verificado.")