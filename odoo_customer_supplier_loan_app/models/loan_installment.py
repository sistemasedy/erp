# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, datetime


class LoanInstallment(models.Model):
    _name = 'loan.installment'
    _description = "Loan Installment"

    name = fields.Char(string="Dia/Fecha", default='DIA/FECHA')

    partner_id = fields.Many2one('res.partner', string="Empresa",
                                 default=lambda self: self.env.user.company_id.id, required=True)
    applied_date = fields.Date(string="Fecha", default=fields.Date.today())
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.user.company_id.id, string="Company", required=True)
    user_id = fields.Many2one(
        'res.users', default=lambda self: self.env.user.id, string="User", readonly=True)
    principal_amount = fields.Float(
        string="Ventas", compute='_compute_overdue_days', digits=(32, 2), store=True)
    salida = fields.Float(
        string="Costos", compute='_compute_overdue_days', digits=(32, 2), store=True)
    balance_on_loans = fields.Float(
        string="Ganancia", compute='_compute_overdue_days', store=True)
    notes = fields.Text(string="Notes")
    start_date = fields.Date(
        string='Fecha de Inicio', default=lambda self: fields.Date.today() - timedelta(days=30))
    end_date = fields.Date(string='Fecha de Fin', default=fields.Date.today)
    currency_id = fields.Many2one(
        'res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    order_line = fields.One2many('report.sale.line', 'order_id', string='Order Lines', states={
                                 'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

    state = fields.Selection([('unpaid', 'Pendiente'), ('approve', 'Aprovado'),
                             ('paid', 'Pagado')], default='unpaid', string="Estado")

    mora = fields.Float(string="Mora", help="Amount",
                        digits=(16, 2))
    sum_parcial = fields.Float(string="Suma Parcial", help="Amount",
                               digits=(16, 2))
    suma_inte = fields.Float(string="Mora", help="Amount",
                             digits=(16, 2))

    anterior_interes = fields.Float(string="I Anterior", help="Amount",
                                    digits=(16, 2))

    sum_paid = fields.Float(string="Pagos", help="Amount",
                            digits=(16, 2))

    sum_paid_int = fields.Float(string="Interes Pagado", help="Amount",
                                digits=(16, 2))
    sum_int_pendiente = fields.Float(string="Intereses Pendiente", help="Amount",
                                     digits=(16, 2))

    @api.depends('order_line')
    def _compute_overdue_days(self):
        # class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        venta = 0
        costo = 0
        balance = 0
        for line in self.order_line:
            venta = venta + line.price_subtotal
            costo = costo + line.price_total
        self.principal_amount = venta
        self.salida = costo
        self.balance_on_loans = venta - costo

    def approve_payment(self):
        self.write({'state': 'approve'})

    def action_payment(self):
        self._create_or_update_purchase_orders()

    def _create_or_update_purchase_orders(self):
        # products = self.env['product.template'].search([])
        product_model = self.env['product.template']
        supplier_info_obj = self.env['product.supplierinfo']
        productssssss = product_model.search([
            ('auto_reorder', '=', True),
            ('main_supplier_id', '!=', False)
        ])

        # Buscar las listas de precios del proveedor seleccionado
        supplier_infos = supplier_info_obj.search(
            [('name', '=', self.partner_id.id)])

        if not supplier_infos:
            raise ValidationError(_("No hay Productos configurados."))

        products_updated = 0

        for supplier_info in supplier_infos:
            product = supplier_info.product_tmpl_id
            reorder_qty = self._get_reorder_quantity(product)
            if reorder_qty > 0:
                self._create_or_update_purchase_order_line(
                    product, reorder_qty)
                products_updated += 1

        # Mostrar un mensaje de éxito al usuario
        if purchase_order_count > 0:
            message = _(
                "Se han creado %s órdenes de compra.") % products_updated
        else:
            message = _("No se ha creado ninguna orden de compra.")

        return {
            'type': 'notification',
            'title': _('Órdenes de Compra Creadas'),
            'message': message,
            'sticky': False,  # El mensaje no se cierra automáticamente
        }

    def _get_reorder_quantity(self, product):
        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', product.id),
            ('location_id.usage', '=', 'internal'),
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('reference', 'ilike', 'WH/POS/%')
        ])
        return abs(sum(stock_moves.mapped('product_qty')))

    def _create_or_update_purchase_order_line(self, product, reorder_qty):
        purchase_order_line_obj = self.env['report.sale.line']

        purchase_order_line = purchase_order_line_obj.search([
            ('order_id', '=', self.id),
            ('product_id', '=', product.id)
        ], limit=1)

        if purchase_order_line:
            purchase_order_line.product_qty = reorder_qty
        else:
            purchase_order_line_obj.create({
                'order_id': self.id,
                'product_id': product.id,
                'price_unit': product.list_price,
                'price_cost': product.standard_price,
                'name': product.name,
                'product_qty': reorder_qty,
                'product_uom': product.uom_po_id.id,
            })

    def reset_draft(self):
        self.write({'state': 'unpaid'})

    def book_interest(self):
        pass

    def generate_excel_report(self):
        """Generates an Excel report for the Loan Installment and its Order Lines."""

        # 1. Prepare Data
        # Get data for the current Loan Installment
        loan_data = self.read(self.ids)[0]
        order_lines_data = self.env['report.sale.line'].search(
            [('order_id', '=', self.id)])

        # 2. Create Workbook and Worksheet
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Loan Installment Report')

        # 3. Define Formats (Optional, for styling)
        header_format = workbook.add_format({'bold': True, 'font_size': 12})
        data_format = workbook.add_format({'font_size': 10})
        title_format = workbook.add_format(
            {'bold': True, 'font_size': 14, 'align': 'center'})

        # 4. Write Report Title
        # Adjusted merge range
        worksheet.merge_range('A1:R1', 'Loan Installment Report', title_format)
        row_index = 2

        # 5. Write Loan Installment Data
        worksheet.write(row_index, 0, 'Loan ID:', header_format)
        # Use loan_data['id']
        worksheet.write(row_index, 1, loan_data['id'], data_format)
        worksheet.write(row_index, 2, 'Fecha:', header_format)
        worksheet.write(row_index, 3, str(
            loan_data['applied_date']), data_format)
        worksheet.write(row_index, 4, 'Empresa:', header_format)
        worksheet.write(row_index, 5, loan_data['partner_id'][1], data_format) if loan_data['partner_id'] else worksheet.write(
            row_index, 5, '', data_format)
        row_index += 1

        worksheet.write(row_index, 0, 'Ventas:', header_format)
        worksheet.write(
            row_index, 1, loan_data['principal_amount'], data_format)
        worksheet.write(row_index, 2, 'Costos:', header_format)
        worksheet.write(row_index, 3, loan_data['salida'], data_format)
        worksheet.write(row_index, 4, 'Ganancia:', header_format)
        worksheet.write(
            row_index, 5, loan_data['balance_on_loans'], data_format)
        row_index += 2

        # 6. Write Order Lines Header
        worksheet.write(row_index, 0, 'Descripción', header_format)
        worksheet.write(row_index, 1, 'Cantidad', header_format)
        worksheet.write(row_index, 2, 'Precio de Venta', header_format)
        worksheet.write(row_index, 3, 'Precio de Compra', header_format)
        worksheet.write(row_index, 4, 'Margen%', header_format)
        worksheet.write(row_index, 5, 'Dif', header_format)
        worksheet.write(row_index, 6, 'Ventas', header_format)
        worksheet.write(row_index, 7, 'Costos', header_format)
        worksheet.write(row_index, 8, 'Ganancia', header_format)
        worksheet.write(row_index, 9, 'Tipo de Producto', header_format)
        worksheet.write(row_index, 10, 'Moneda', header_format)
        worksheet.write(row_index, 11, 'Compañía', header_format)
        worksheet.write(row_index, 12, 'Estado', header_format)
        worksheet.write(row_index, 13, 'Socio', header_format)
        worksheet.write(row_index, 14, 'Cantidad Total', header_format)
        worksheet.write(row_index, 15, 'Unidad de Medida', header_format)
        worksheet.write(row_index, 16, 'Producto', header_format)
        row_index += 1

        # 7. Write Order Lines Data
        for line in order_lines_data:
            worksheet.write(row_index, 0, line.name, data_format)
            worksheet.write(row_index, 1, line.product_qty, data_format)
            worksheet.write(row_index, 2, line.price_unit, data_format)
            worksheet.write(row_index, 3, line.price_cost, data_format)
            worksheet.write(row_index, 4, line.price_margin, data_format)
            worksheet.write(row_index, 5, line.price_gan, data_format)
            worksheet.write(row_index, 6, line.price_subtotal, data_format)
            worksheet.write(row_index, 7, line.price_total, data_format)
            worksheet.write(row_index, 8, line.price_balan, data_format)
            worksheet.write(row_index, 9, line.product_type or '', data_format)
            worksheet.write(
                row_index, 10, line.currency_id.name if line.currency_id else '', data_format)
            worksheet.write(
                row_index, 11, line.company_id.name if line.company_id else '', data_format)
            worksheet.write(row_index, 12, line.state or '', data_format)
            worksheet.write(
                row_index, 13, line.partner_id.name if line.partner_id else '', data_format)
            worksheet.write(row_index, 14, line.product_uom_qty, data_format)
            worksheet.write(
                row_index, 15, line.product_uom.name if line.product_uom else '', data_format)
            worksheet.write(
                row_index, 16, line.product_id.name if line.product_id else '', data_format)
            row_index += 1

        # 8. Finish and Return
        workbook.close()
        output.seek(0)
        excel_file = base64.b64encode(output.read())
        self.env['sale.report.xlsx'].create({  # Changed to sale.report.xlsx
            'excel_file': excel_file,
            'file_name': 'Loan Installment Report.xlsx',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=sale.report.xlsx&id=%s&filename=%s' % (  # Changed to sale.report.xlsx
                self.env['sale.report.xlsx'].id, 'Loan Installment Report.xlsx'),
            'target': 'new',
            'disposition': 'attachment',
        }

    @api.model
    def _action_generate_sale_report_excel(self):
        return self.generate_excel_report()

    def action_update_supplier_products(self):
        """
        Actualiza la lista de precios del proveedor basándose en las cotizaciones existentes.
        """
        self.ensure_one()
        supplier_info_obj = self.env['product.supplierinfo']
        purchase_order_line_obj = self.env['purchase.order.line']

        # 1. Buscar todas las líneas de órdenes de compra (cotizaciones) para este proveedor
        purchase_order_lines = purchase_order_line_obj.search([
            ('order_id.partner_id', '=', self.partner_id.id),
            # Asegurar que hay un producto asociado
            ('product_id', '!=', False),
            # Asegurar que el precio unitario es válido
            ('price_unit', '>', 0),
        ])

        products_updated = 0

        # 2. Iterar sobre las líneas de órdenes de compra y actualizar la lista de precios
        for line in purchase_order_lines:
            product = line.product_id.product_tmpl_id  # Obtener el product template
            price = line.price_unit

            # 3. Buscar si ya existe una entrada para este proveedor y producto
            existing_supplier_info = supplier_info_obj.search([
                ('name', '=', self.partner_id.id),
                ('product_tmpl_id', '=', product.id),
            ], limit=1)

            if existing_supplier_info:
                # 4. Si existe, actualizar el precio
                existing_supplier_info.write({'price': price})
            else:
                # 5. Si no existe, crear una nueva entrada
                supplier_info_obj.create({
                    'name': self.partner_id.id,
                    'product_tmpl_id': product.id,
                    'price': price,
                })
                products_updated += 1

        # Mostrar un mensaje de éxito al usuario
        if purchase_order_count > 0:
            message = _(
                "Se han actualizado %s Productos.") % products_updated
        else:
            message = _("No se ha actualizado ningun producto.")

        return {
            'type': 'notification',
            'title': _('Órdenes de Compra Creadas'),
            'message': message,
            'sticky': False,  # El mensaje no se cierra automáticamente
        }

    def create_purchase_orders(self):
        """
        Crea órdenes de compra a partir de las líneas de pedido en self.order_line.
        """
        purchase_order_obj = self.env['purchase.order']
        purchase_order_line_obj = self.env['purchase.order.line']

        # Agrupar las líneas de pedido por proveedor para crear una orden de compra por proveedor.
        orders_by_partner = {}
        products_updated = 0

        for line in self.order_line:
            if line.partner_id not in orders_by_partner:
                orders_by_partner[line.partner_id] = []
            orders_by_partner[line.partner_id].append(line)

        for partner, lines in orders_by_partner.items():
            # Crear la orden de compra
            purchase_order_vals = {
                'partner_id': partner.id,
                # Asegurar que la orden de compra esté en la misma compañía que el reporte.
                'company_id': self.company_id.id,
                'currency_id': self.currency_id.id,  # Asegurar la misma moneda
                'origin': self.name,  # Referencia al reporte de venta
            }
            purchase_order = purchase_order_obj.create(purchase_order_vals)

            # Crear las líneas de la orden de compra
            for line in lines:
                purchase_order_line_vals = {
                    'order_id': purchase_order.id,
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    'price_unit': line.price_cost,  # Usar el precio de costo
                    'name': line.name,
                    'product_uom': line.product_uom.id,
                    'date_planned': fields.Date.today(),  # Puedes ajustar esto
                }
                purchase_order_line_obj.create(purchase_order_line_vals)
                products_updated += 1

        # Mostrar un mensaje de éxito al usuario
        if purchase_order_count > 0:
            message = _(
                "Se han creado %s órdenes de compra.") % products_updated
        else:
            message = _("No se ha creado ninguna orden de compra.")

        return {
            'type': 'notification',
            'title': _('Órdenes de Compra Creadas'),
            'message': message,
            'sticky': False,  # El mensaje no se cierra automáticamente
        }


class ReportSaleLine(models.Model):
    """Loan repayments """
    _name = "report.sale.line"
    _description = "Report Sale Line"

    name = fields.Char(string="Descripcion")
    order_id = fields.Many2one('loan.installment', string='Order Reference',
                               index=True, required=True, ondelete='cascade')

    product_qty = fields.Float(
        string='Cantidad', digits='Product Unit of Measure', required=True)
    price_unit = fields.Float(string='Precio de Venta',
                              required=True, digits='Product Price')
    price_cost = fields.Float(
        string='Precio de Compra', digits='Product Price')
    price_margin = fields.Float(string='Margen%', digits='Product Price')
    price_gan = fields.Float(string='Dif', digits='Product Price')

    price_subtotal = fields.Monetary(
        compute='_compute_amount', string='Ventas', store=True, currency_field='currency_id')
    price_total = fields.Monetary(
        compute='_compute_amount', string='Costos', store=True, currency_field='currency_id')
    price_balan = fields.Float(string='Ganancia', digits='Product Price')

    product_type = fields.Selection(
        related='product_id.detailed_type', readonly=True)
    currency_id = fields.Many2one(
        'res.currency', related='order_id.currency_id', store=True, readonly=True, string='Currency')
    company_id = fields.Many2one(
        'res.company', related='order_id.company_id', string='Company', store=True, readonly=True)
    state = fields.Selection(related='order_id.state', store=True)
    partner_id = fields.Many2one(
        'res.partner', related='order_id.partner_id', string='Partner', readonly=True, store=True)
    product_uom_qty = fields.Float(
        string='Total Quantity', compute='_compute_product_uom_qty', store=True)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
                                  domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(
        related='product_id.uom_id.category_id')
    product_id = fields.Many2one('product.product', string='Producto', domain=[
                                 ('purchase_ok', '=', True)], change_default=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        costo_alterno = 0
        costo_disponible = 0
        for line in self:
            line.price_subtotal = line.product_qty * line.price_unit
            if line.price_cost > 0:
                line.price_total = (line.product_qty * line.price_cost)
                if line.price_unit > 1:
                    line.price_gan = (line.price_unit - line.price_cost)
                    line.price_margin = (
                        ((line.price_unit - line.price_cost)/line.price_cost)*100)
                if line.price_unit == 1:
                    line.price_gan = 0
                    line.price_margin = 0
            if line.price_cost == 0:
                line.price_total = ((line.product_qty * line.price_unit) -
                                    ((line.product_qty * line.price_unit) * 20/100))
                if line.price_unit > 1:
                    line.price_gan = ((line.price_unit)*(20/100))
                    line.price_margin = 20
                if line.price_unit == 1:
                    line.price_gan = 0
                    line.price_margin = 0

            line.price_balan = line.price_subtotal - line.price_total


class ProductProduct(models.Model):
    _inherit = 'product.template'

    main_supplier_id = fields.Many2one('res.partner', string='Proveedor Principal', domain=[(
        'supplier_rank', '>', 0)], help='Proveedor principal para reordenar automáticamente')
    auto_reorder = fields.Boolean(string='Reordenar Automáticamente')
    ignore_product = fields.Boolean(string='Ignoral', default=False)
    product_pack = fields.Float(string='Cantida Paquete', store=True)
    qty_pack = fields.Float(string='Pedido', store=True)
