# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
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
# #############################################################################
from odoo import api, fields, models
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None


class PosOrder(models.Model):
    """Inherited this model to create a function to get the corresponding
       invoice for pos order"""
    _inherit = 'pos.order'

    #order_ncf = fields.Char(string='NCF')
    #order_ncf = fields.Char(string='NCF')
    client_name = fields.Char(string='Nombre del Cliente')
    client_vat = fields.Char(string='NIF/CIF del Cliente')
    client_address = fields.Char(string='Dirección del Cliente')
    invoice_number = fields.Char(string='Número de Factura')
    invoice_date = fields.Date(string='Fecha de Factura')
    invoice_total = fields.Float(string='Total de Factura', digits=(16, 2))

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res.update({
            'client_name': ui_order.get('client_name'),
            'client_vat': ui_order.get('client_vat'),
            'client_address': ui_order.get('client_address'),
            'invoice_number': ui_order.get('invoice_number'),
            'invoice_date': ui_order.get('invoice_date'),
            'invoice_total': ui_order.get('invoice_total'),
        })
        return res

    @api.model
    def create(self, vals):
        order = super(PosOrder, self).create(vals)
        order.update_order_fields()
        return order

    def update_order_fields(self):
        # Buscar la factura asociada a este pedido
        move = self.env['account.move'].search([('invoice_origin', '=', self.name)], limit=1)
        
        if move:
            # Preparar los valores a actualizar
            update_values = {
                'client_name': move.partner_id.name,
                'client_vat': move.partner_id.vat,
                'client_address': move.partner_id.contact_address,
                'invoice_number': move.name,
                'invoice_date': move.invoice_date,
                'invoice_total': move.amount_total,
            }
            
            # Actualizar el pedido con los valores obtenidos de la factura
            self.write(update_values)

    @api.model
    def get_invoice(self, id):
        """Retrieve the corresponding invoice details based on the provided ID.
        Args:
        id (int): The ID of the invoice.
        Returns:
        dict: A dictionary containing the invoice details.

        ids = pos.id + 1

        pos_id = ids

        
        """
        pos_id = self.search([('pos_reference', '=', id)])
        
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        invoice_id = self.env['account.move'].search(
            [('invoice_origin', '=', pos_id.name)])
        return {
            'invoice_id': invoice_id.id,
            'invoice_type': invoice_id.l10n_latam_document_type_id.report_name,
            'invoice_fiscal': invoice_id.l10n_do_fiscal_number,
            'invoice_name': invoice_id.name,
            'base_url': base_url,
            'is_qr_code': invoice_id.account_barcode}
