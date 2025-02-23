# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseFiscalReport(models.Model):
    _inherit = 'purchase.order'

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


    @api.depends('amount_untaxed', 'amount_tax', 'ncf_check')
    def _compute_ncf_amounts(self):
        for order in self:
            if order.ncf_check:
                pass
            else:
                order.ncf_amount_purchase = order.amount_untaxed
                order.ncf_tax = order.amount_tax


    @api.depends('ncf_amount_purchase', 'ncf_tax')
    def _compute_ncf_total(self):
        for order in self:
            order.ncf_total = order.ncf_amount_purchase + order.ncf_tax



    @api.onchange('date_order')
    def _onchange_date_order(self):
        for order in self:
            if order.date_order:
                order.ncf_day = order.date_order.strftime('%d')
                order.ncf_year_month = order.date_order.strftime('%Y%m')
            else:
                order.ncf_day = False
                order.ncf_year_month = False



    

    @api.onchange('ncf_check')
    def _onchange_ncf_check(self):
        self._compute_ncf_amounts()