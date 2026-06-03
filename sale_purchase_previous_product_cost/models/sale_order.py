# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, api, fields
from odoo.exceptions import UserError


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

