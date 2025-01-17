from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    overdue_days_limit = fields.Integer(
        string="Límite de Días para Facturas Vencidas",
        default=120,
        help="Número de días que se considerarán para evaluar si una factura está vencida."
    )


