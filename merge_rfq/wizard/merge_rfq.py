# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#

#
###############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class MergeRfq(models.TransientModel):
    """Wizard to merge the RFQs"""
    _name = 'merge.rfq'
    _description = 'Merge RFQ'

    merge_type = fields.Selection(selection=[
        ('cancel_and_new', 'Cancel all selected purchase order and Create new order'),
        ('delete_and_new', 'Delete all selected purchase order and Create new order'),
        ('cancel_and_merge', 'Merge order on existing selected order and cancel others'),
        ('delete_and_merge', 'Merge order on existing selected order and delete others')],
        default='cancel_and_new', help='Select which type of merge is to done.'
    )
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', help='Select RFQ to which others to be merged')
    start_date = fields.Date(string='Fecha de Inicio', default=lambda self: fields.Date.today() - timedelta(days=30))
    end_date = fields.Date(string='Fecha de Fin', default=fields.Date.today)
    partner_id = fields.Many2one('res.partner', string='Proveedor')
    select_all_suppliers = fields.Boolean(string='Desactivar todos los Proveedores', default=True)

    def update_quant_products(self):
        self.ensure_one()
        products_updated = 0

        internal_location = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        supplier_infos = self.env['product.supplierinfo'].search([('name', '=', self.partner_id.id)])

        for supplier_info in supplier_infos:
            product = supplier_info.product_tmpl_id
            if product:
                self._adjust_quantities_to_zero(product.product_variant_ids.ids, internal_location)
                products_updated += 1

        return self._reload_client_with_message(f'{products_updated} productos actualizados correctamente.')

    def _adjust_quantities_to_zero(self, product_variant_ids, internal_location):
        stock_quant_obj = self.env['stock.quant']
        stock_move_obj = self.env['stock.move']

        while True:
            adjustments_needed = False
            quants = stock_quant_obj.search([('product_id', 'in', product_variant_ids)])
            for quant in quants:
                if quant.quantity != 0:
                    adjustments_needed = True
                    self._create_stock_move(quant, internal_location)
            if not adjustments_needed:
                break

    def _create_stock_move(self, quant, internal_location):
        stock_move_obj = self.env['stock.move']
        location_id, location_dest_id = (quant.location_id.id, internal_location.id) if quant.quantity > 0 else (internal_location.id, quant.location_id.id)
        
        stock_move = stock_move_obj.create({
            'name': f'Adjustment for {quant.product_id.name}',
            'product_id': quant.product_id.id,
            'product_uom_qty': abs(quant.quantity),
            'product_uom': quant.product_id.uom_id.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'state': 'confirmed',
        })
        stock_move._action_confirm()
        stock_move._action_assign()
        stock_move.move_line_ids.write({'qty_done': abs(quant.quantity)})
        stock_move._action_done()

    def update_supplier_products(self):
        self.ensure_one()
        products_updated = 0
        supplier_infos = self.env['product.supplierinfo'].search([('name', '=', self.partner_id.id)])

        for supplier_info in supplier_infos:
            product = supplier_info.product_tmpl_id
            if product:
                product.write({
                    'main_supplier_id': self.partner_id.id,
                    'auto_reorder': True,
                })
                products_updated += 1

        return self._reload_client_with_message(f'{products_updated} productos actualizados correctamente.')

    def create_or_update_purchase_orders(self):
        automate_purchase_quan = self.env['ir.config_parameter'].sudo().get_param('automate_purchase_quan')
        if automate_purchase_quan:
            self.create_or_update_purchase_orders2()
        else:
            raise ValidationError(_("Debes Activar la automatización en Configuración."))

    def create_or_update_purchase_orders2(self):
        if self.select_all_suppliers:
            self.create_or_update_purchase_orders_by_supplier()
        else:
            self.create_or_update_purchase_orders_by_selected_supplier()

    def create_or_update_purchase_orders_by_selected_supplier(self):
        self._create_or_update_purchase_orders(lambda product: product.main_supplier_id == self.partner_id)

    def create_or_update_purchase_orders_by_supplier(self):
        self._create_or_update_purchase_orders(lambda product: True)

    def _create_or_update_purchase_orders(self, supplier_filter):
        products = self.env['product.template'].search([
            ('auto_reorder', '=', True),
            ('main_supplier_id', '!=', False),
            ('ignore_product', '=', False)
        ])

        if not products:
            raise ValidationError(_("No hay Productos configurados."))

        suppliers = {}
        for product in products:
            if supplier_filter(product):
                supplier = product.main_supplier_id
                if supplier not in suppliers:
                    suppliers[supplier] = []
                suppliers[supplier].append(product)

        if not suppliers:
            raise ValidationError(_("El Proveedor o los Productos no están configurados."))

        products_updated = 0
        for supplier, products in suppliers.items():
            purchase_order = self._get_or_create_purchase_order(supplier)
            for product in products:
                reorder_qty = self._get_reorder_quantity(product)
                if reorder_qty > 0:
                    self._create_or_update_purchase_order_line(purchase_order, product, reorder_qty)
                    products_updated += 1

        return self._reload_client_with_message(f'{products_updated} ordenes creadas o actualizadas correctamente.')

    def _get_or_create_purchase_order(self, supplier):
        purchase_order_obj = self.env['purchase.order']
        purchase_order = purchase_order_obj.search([
            ('partner_id', '=', supplier.id),
            ('state', '=', 'draft'),
            ('automation_created', '=', True)
        ], limit=1)

        if not purchase_order:
            purchase_order = purchase_order_obj.create({
                'partner_id': supplier.id,
                'order_line': [],
                'origin': 'Automated Reorder',
                'automation_created': True
            })
        return purchase_order

    def _get_reorder_quantity(self, product):
        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', product.id),
            ('location_id.usage', '=', 'internal'),
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('reference', 'ilike', 'WH/POS/%')
        ])
        return abs(sum(stock_moves.mapped('product_qty')))

    def _create_or_update_purchase_order_line(self, purchase_order, product, reorder_qty):
        purchase_order_line_obj = self.env['purchase.order.line']
        supplier_info = product.seller_ids.filtered(lambda s: s.name == product.main_supplier_id)[0]

        purchase_order_line = purchase_order_line_obj.search([
            ('order_id', '=', purchase_order.id),
            ('product_id', '=', product.id)
        ], limit=1)

        if purchase_order_line:
            purchase_order_line.product_qty = reorder_qty
        else:
            purchase_order_line_obj.create({
                'order_id': purchase_order.id,
                'product_id': product.id,
                'name': product.name,
                'product_qty': reorder_qty,
                'product_uom': product.uom_po_id.id,
                'price_unit': supplier_info.price,
                'date_planned': fields.Date.today(),
            })

    def _reload_client_with_message(self, message):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'name': 'Productos Actualizados',
            'params': {'message': message}
        }

    @api.onchange('merge_type')
    def _onchange_merge_type(self):
        for order in self:
            order.purchase_order_id = False
            if order.merge_type in ['cancel_and_merge', 'delete_and_merge']:
                return {
                    'domain': {'purchase_order_id': [("id", "in", self._context.get("active_ids"))]}
                }

    def action_merge_orders(self):
        purchase_orders = self.env["purchase.order"].browse(self._context.get("active_ids", []))
        if len(purchase_orders) < 2:
            raise UserError(_("Please select at least two purchase orders."))
        if any(order.state not in ["draft", "sent"] for order in purchase_orders):
            raise UserError(_("Please select Purchase orders which are in RFQ or RFQ sent state."))

        if self.merge_type in ['cancel_and_new', 'delete_and_new']:
            self._create_new_purchase_order_from_merge(purchase_orders)
        else:
            self._merge_into_existing_order(purchase_orders)

    def _create_new_purchase_order_from_merge(self, purchase_orders):
        new_po = self.env["purchase.order"].create({"partner_id": self.partner_id.id})
        for order in purchase_orders:
            self._copy_order_lines_to_new_order(order, new_po)
            self._cancel_or_delete_order(order)
        
    def _copy_order_lines_to_new_order(self, order, new_po):
        for line in order.order_line:
            existing_line = new_po.order_line.filtered(
                lambda new_line: line.product_id == new_line.product_id and line.price_unit == new_line.price_unit)
            if existing_line:
                existing_line.product_qty += line.product_qty
            else:
                line.copy(default={"order_id": new_po.id})

    def _cancel_or_delete_order(self, order):
        order.sudo().button_cancel()
        if self.merge_type == "delete_and_new":
            order.sudo().unlink()

    def _merge_into_existing_order(self, purchase_orders):
        selected_po = self.purchase_order_id
        for order in purchase_orders:
            if order != selected_po:
                self._copy_order_lines_to_new_order(order, selected_po)
                self._cancel_or_delete_order(order)



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    automation_created = fields.Boolean(
        string='Creado por Automatización', default=False)

    is_selected = fields.Boolean(string="Auto Pproceso", default=False)

    def action_mark_selected(self):
        # Verifica que haya al menos una orden seleccionada
        if not self:
            raise UserError(_("Please select at least one purchase order."))

        # Actualiza el campo booleano is_selected de False a True
        for order in self:
            order.is_selected = True
            # Confirmar la orden de compra (si está en estado draft o RFQ)
            if order.state in ['draft', 'sent']:
                order.button_confirm()

            # Crear la factura correspondiente
            if order.state == 'purchase':  # Verifica si la orden está confirmada
                invoice = order._create_invoices()

                # Actualizar la fecha de la factura con la fecha de la cotización
                invoice.invoice_date = order.date_order

                # Confirmar la factura (si es necesario)
                invoice.action_post()


    def action_mark_selected(self):
        # Verifica que haya al menos una orden seleccionada
        if not self:
            raise UserError(_("Please select at least one purchase order."))

        for order in self:
            # Marcar el campo booleano is_selected como True
            order.is_selected = True
            
            # Confirmar la orden de compra si está en estado borrador
            if order.state == 'draft':
                order.button_confirm()

            # Crear la factura para la orden de compra confirmada
            if order.state == 'purchase':  # Verifica si la orden está confirmada
                invoice = self.env['account.move'].create({
                    'move_type': 'in_invoice',  # Tipo de factura de proveedor
                    'partner_id': order.partner_id.id,  # Proveedor asociado
                    'invoice_origin': order.name,  # Origen de la factura
                    'invoice_date': order.date_order,  # Fecha de la cotización
                    'invoice_line_ids': [(0, 0, {
                        'name': line.name,
                        'quantity': line.product_qty,
                        'price_unit': line.price_unit,
                        'product_id': line.product_id.id,
                        'account_id': line.product_id.categ_id.property_account_expense_categ_id.id,
                    }) for line in order.order_line],
                })

            # Publicar la factura (opcional, si se requiere)
            invoice.action_post()

class ProductProduct(models.Model):
    _inherit = 'product.template'

    main_supplier_id = fields.Many2one('res.partner', string='Proveedor Principal', domain=[(
        'supplier_rank', '>', 0)], help='Proveedor principal para reordenar automáticamente')
    auto_reorder = fields.Boolean(string='Reordenar Automáticamente')
    ignore_product = fields.Boolean(string='Ignoral', default=False)

class PurchaseOrderAutomation(models.TransientModel):
    _name = 'purchase.order.automation'
    _description = 'Automatización de Órdenes de Compra'

    start_date = fields.Date(
        string='Fecha de Inicio', default=lambda self: fields.Date.today() - timedelta(days=30))
    end_date = fields.Date(string='Fecha de Fin', default=fields.Date.today)
    

    # Agrupar productos por proveedor principal
    def create_or_update_purchase_orders(self):
        product_model = self.env['product.template']
        products = product_model.search([
            ('auto_reorder', '=', True),
            ('main_supplier_id', '!=', False)
        ])

        purchase_order_obj = self.env['purchase.order']
        purchase_order_line_obj = self.env['purchase.order.line']

        suppliers = {}

        # Agrupar productos por proveedor principal
        for product in products:
            supplier = product.main_supplier_id
            if supplier not in suppliers:
                suppliers[supplier] = []
            suppliers[supplier].append(product)

        for supplier, products in suppliers.items():
            # Buscar o crear una orden de compra para el proveedor
            purchase_order = purchase_order_obj.search([
                ('partner_id', '=', supplier.id),
                ('state', '=', 'draft'),
                # Solo procesar órdenes creadas por automatización
                ('automation_created', '=', True)
            ], limit=1)

            if not purchase_order:
                purchase_order = purchase_order_obj.create({
                    'partner_id': supplier.id,
                    'order_line': [],
                    'automation_created': True  # Marcar la orden como creada por automatización
                })

            for product in products:
                supplier_info = product.seller_ids.filtered(
                    lambda s: s.name == supplier)
                if supplier_info:
                    supplier_info = supplier_info[0]

                    # Filtrar los movimientos de stock dentro del rango de fechas y por referencias de ventas
                    stock_moves = self.env['stock.move'].search([
                        ('product_id', '=', product.id),
                        ('location_id.usage', '=', 'internal'),
                        ('date', '>=', self.start_date),
                        ('date', '<=', self.end_date),
                        # Filtrar por referencias de POS o ventas
                        ('reference', 'ilike', 'POS/%') | ('reference', 'ilike', 'SO/%')
                    ])

                    reorder_qty = sum(stock_moves.mapped('product_qty')) * -1

                    if reorder_qty > 0:
                        purchase_order_line = purchase_order_line_obj.search([
                            ('order_id', '=', purchase_order.id),
                            ('product_id', '=', product.id)
                        ], limit=1)
                        if purchase_order_line:
                            purchase_order_line.product_qty += reorder_qty
                        else:
                            purchase_order_line_obj.create({
                                'order_id': purchase_order.id,
                                'product_id': product.id,
                                'name': product.name,
                                'product_qty': reorder_qty,
                                'product_uom': product.uom_po_id.id,
                                'price_unit': supplier_info.price,
                                'date_planned': fields.Date.today(),
                            })

        self._compute_totals()



class ResPartnerSupplierUpdate(models.TransientModel):
    _name = 'supplier.update'
    _description = 'Actualizar Proveedor Principal y Reordenar Automáticamente'

    partner_id = fields.Many2one('res.partner', string='Proveedor', domain=[('supplier_rank', '>', 0)], required=True)

    def update_supplier_products(self):
        self.ensure_one()
        supplier_info_obj = self.env['product.supplierinfo']
        products_updated = 0

        # Buscar las listas de precios del proveedor seleccionado
        supplier_infos = supplier_info_obj.search([('name', '=', self.partner_id.id)])
        
        for supplier_info in supplier_infos:
            product = supplier_info.product_tmpl_id
            if product:
                product.write({
                    'main_supplier_id': self.partner_id.id,
                    'auto_reorder': True,
                })
                products_updated += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'name': 'Productos Actualizados',
            'params': {
                'message': f'{products_updated} productos actualizados correctamente.'
            }
        }


