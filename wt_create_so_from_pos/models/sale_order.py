from odoo import _, api, fields, models
import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_pos_created = fields.Boolean(string='Create from POS')


    @api.model
    def craete_saleorder_from_pos(self, orderdetails):
        vals = {}
        saleorder_id = self.env['sale.order'].create({
            'partner_id': orderdetails.get('partner_id'),
            'date_order': datetime.date.today(),
            'is_pos_created': True,
            'state': 'draft',
            'amount_tax': orderdetails.get('tax_amount'),
        })
        vals['name'] = saleorder_id.name
        vals['id'] = saleorder_id.id

        for key, data in orderdetails.items():
            if key not in ['partner_id', 'tax_amount']:
                current_dict = data
                if isinstance(current_dict, dict):  # Verificar que es un diccionario
                    saleorder_id.order_line = [(0, 0, {
                        'product_id': current_dict.get('product'),
                        'product_uom_qty': current_dict.get('quantity'),
                        'price_unit': current_dict.get('price'),
                        'discount': current_dict.get('discount'),
                    })]
        return vals