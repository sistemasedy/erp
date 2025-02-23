# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseFiscal(models.Model):
    _inherit = "purchase.order"

    ncf_tax_p = fields.Monetary(string='Impuesto NCF')

    ncf_amount_purchase_p = fields.Monetary(string='Monto de Venta NCF')
    ncf_total_p = fields.Monetary(string='Total NCF')
    ncf_day_p = fields.Char(string='Día NCF', help="Día de la transacción para el NCF.")
    ncf_year_month_p = fields.Char(string='Año/Mes NCF', help="Año y mes de la transacción para el NCF.")
    ncf_check_p = fields.Boolean(string='Verificación NCF', help="Indica si el NCF ha sido verificado.")

    check_complete_p = fields.Boolean(string='Completado', help="Indica si el registro está completo.")
    check_verificate_p = fields.Boolean(string='Verificado', help="Indica si el registro ha sido verificado.")



class PurchaseFiscalReport(models.Model):
    _name = 'purchase.fiscal.report'
    _inherit = 'purchase.order' # purchase.order, NOT sale.order

    