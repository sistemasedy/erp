from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    automation_created = fields.Boolean(
        string='Creado por Automatización', default=False)
