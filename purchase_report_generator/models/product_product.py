from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.template'

    main_supplier_id = fields.Many2one('res.partner', string='Proveedor Principal', domain=[(
        'supplier_rank', '>', 0)], help='Proveedor principal para reordenar automáticamente')
    auto_reorder = fields.Boolean(string='Reordenar Automáticamente')
