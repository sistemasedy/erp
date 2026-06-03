# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare


class ConstructionSubcontract(models.Model):
    """
    Modelo principal para gestionar los subcontratos y las cubicaciones (avances de obra)
    vinculados a proyectos y subcontratistas.
    """
    _name = 'construction.subcontract'
    _description = 'Subcontrato de Construcción'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, name'

    # ============================
    # CAMPOS BÁSICOS
    # ============================
    name = fields.Char(
        string='Número de Contrato',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nuevo'),
        tracking=True,
        help='Referencia única del subcontrato generada por secuencia.'
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Ajustero/Subcontratista',
        required=True,
        domain="[('supplier_rank', '>', 0)]",
        tracking=True
    )

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Proyecto',
        required=True,
        tracking=True
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Compañía',
        default=lambda self: self.env.company,
        required=True
    )

    currency_id = fields.Many2one(
        related='company_id.currency_id',
        string='Moneda',
        readonly=True
    )

    # ============================
    # CAMPOS DE CONTRATO Y PRECIOS
    # ============================
    work_description = fields.Text(
        string='Descripción del Trabajo',
        required=True,
        help='Ej: Instalación de andamios en Torre Nivel 3-7'
    )

    # Se usa fields.Char y se definen las unidades en data/measurement_units.xml
    # para permitir una configuración dinámica.
    measurement_unit = fields.Char(
        string='Unidad de Medida',
        required=True,
        help='Ej: m2, ml, unidad.'
        # NOTA: Si usas 'Selection' como tenías, no necesitas el archivo XML
        # Si quieres que sea configurable, úsalo como fields.Char y luego un modelo 'construction.measurement.unit'
        # Mantendremos Char por ahora, asumiendo que data/measurement_units.xml carga los valores predeterminados.
    )

    unit_price = fields.Monetary(
        string='Precio Unitario',
        required=True,
        currency_field='currency_id',
        tracking=True
    )

    estimated_quantity = fields.Float(
        string='Cantidad Estimada',
        required=True,
        digits='Product Unit of Measure',
        tracking=True
    )

    contract_amount = fields.Monetary(
        string='Monto Total Contrato',
        compute='_compute_contract_amount',
        store=True,
        currency_field='currency_id',
        help='Monto total si se ejecuta la cantidad estimada al precio unitario.'
    )

    guarantee_percentage = fields.Float(
        string='% Retención de Garantía',
        default=20.0,
        required=True,
        digits='Discount',  # Usamos la precisión de descuentos
        tracking=True
    )

    # ============================
    # CAMPOS DE FECHAS
    # ============================
    date_start = fields.Date(
        string='Fecha Inicio',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )

    date_end = fields.Date(
        string='Fecha Estimada Fin',
        tracking=True
    )

    # ============================
    # CAMPOS DE AVANCE Y CÁLCULOS
    # ============================
    progress_ids = fields.One2many(
        comodel_name='construction.work.progress',
        inverse_name='subcontract_id',
        string='Avances de Obra Validados'
    )

    # --- Totales Computados (Solo avances en estado 'validated') ---
    total_quantity_done = fields.Float(
        string='Cantidad Total Ejecutada',
        compute='_compute_totals',
        store=True,
        digits='Product Unit of Measure'
    )

    total_amount_invoiced = fields.Monetary(
        string='Total Facturado Neto (Avances)',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id',
        help='Monto neto facturado por los avances validados (sin incluir impuestos).'
    )

    total_guarantee_retained = fields.Monetary(
        string='Total Garantía Retenida',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id',
        help='Suma de todas las retenciones aplicadas a los avances.'
    )

    total_paid = fields.Monetary(
        string='Total Pagado a Subcontratista',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id',
        help='Monto total pagado (Avance - Retención).'
    )

    # Campo para la Liberación de Garantía
    guarantee_released = fields.Boolean(
        string='Garantía Liberada',
        copy=False,
        tracking=True,
        default=False,
        help='Indica si la factura de liberación de garantía ha sido creada.'
    )

    # Campo calculado para el % completado
    percentage_completed = fields.Float(
        string='% Completado',
        compute='_compute_percentage',
        store=True,
        digits=(16, 2)
    )

    # ============================
    # CAMPOS DE ESTADO Y FLUIDEZ
    # ============================
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('active', 'Activo'),
            ('completed', 'Completado'),
            ('cancelled', 'Cancelado'),
        ],
        string='Estado',
        default='draft',
        required=True,
        tracking=True
    )

    notes = fields.Html(string='Términos y Condiciones')

    # ============================
    # MÉTODOS COMPUTADOS Y DEPENDENCIAS
    # ============================
    @api.depends('unit_price', 'estimated_quantity')
    def _compute_contract_amount(self):
        for record in self:
            record.contract_amount = record.unit_price * record.estimated_quantity

    @api.depends('progress_ids.quantity_done', 'progress_ids.amount',
                 'progress_ids.guarantee_amount', 'progress_ids.state',
                 'unit_price')  # Añadido 'unit_price' aunque no es estrictamente necesario, da contexto.
    def _compute_totals(self):
        """Calcula las cantidades y montos totales usando solo avances 'validated'."""
        for record in self:
            # Filtramos solo los avances que han sido validados
            validated_progress = record.progress_ids.filtered(
                lambda p: p.state == 'validated'
            )

            # Suma de la cantidad ejecutada
            total_qty = sum(validated_progress.mapped('quantity_done'))

            # Suma del monto facturado (Monto del Avance)
            total_amount = sum(validated_progress.mapped('amount'))

            # Suma de la garantía retenida
            total_guarantee = sum(
                validated_progress.mapped('guarantee_amount'))

            record.total_quantity_done = total_qty
            record.total_amount_invoiced = total_amount
            record.total_guarantee_retained = total_guarantee
            # El total pagado es el monto de avance menos la retención
            record.total_paid = total_amount - total_guarantee

    @api.depends('total_quantity_done', 'estimated_quantity')
    def _compute_percentage(self):
        """Calcula el porcentaje completado basado en la cantidad ejecutada."""
        for record in self:
            if float_compare(record.estimated_quantity, 0, precision_digits=3) > 0:
                record.percentage_completed = min(
                    (record.total_quantity_done / record.estimated_quantity) * 100,
                    100.0
                )
            else:
                record.percentage_completed = 0.0

    # ============================
    # VALIDACIONES Y CONSTRAINTS
    # ============================
    @api.constrains('unit_price')
    def _check_unit_price(self):
        for record in self:
            if float_compare(record.unit_price, 0, precision_digits=2) <= 0:
                raise ValidationError(
                    _('El precio unitario debe ser mayor a cero.')
                )

    @api.constrains('estimated_quantity')
    def _check_estimated_quantity(self):
        for record in self:
            if float_compare(record.estimated_quantity, 0, precision_digits=3) <= 0:
                raise ValidationError(
                    _('La cantidad estimada debe ser mayor a cero.')
                )

    @api.constrains('guarantee_percentage')
    def _check_guarantee_percentage(self):
        for record in self:
            if not (0 <= record.guarantee_percentage <= 100):
                raise ValidationError(
                    _('El porcentaje de garantía debe estar entre 0%% y 100%%.')
                )

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_end and record.date_start > record.date_end:
                raise ValidationError(
                    _('La fecha de fin no puede ser anterior a la fecha de inicio.')
                )

    # ============================
    # MÉTODOS DE NEGOCIO Y FLUJO DE TRABAJO
    # ============================
    @api.model
    def create(self, vals):
        """Asigna el número de secuencia al crear."""
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.subcontract'
            ) or _('Nuevo')
        return super().create(vals)

    def action_activate(self):
        """Activar el contrato (Pasa de Borrador a Activo)."""
        for record in self:
            if record.state != 'draft':
                raise UserError(
                    _('Solo se pueden activar contratos en borrador.')
                )
            record.state = 'active'
            record.message_post(
                body=_('Contrato activado por %s') % self.env.user.name
            )

    def action_complete(self):
        """Completar el contrato (Pasa de Activo a Completado)."""
        for record in self:
            if record.state != 'active':
                raise UserError(
                    _('Solo se pueden completar contratos activos.')
                )
            record.state = 'completed'
            record.message_post(
                body=_('Contrato completado. Cantidad Total Ejecutada: %.2f %s') % (
                    record.total_quantity_done,
                    record.measurement_unit
                )
            )

    def action_cancel(self):
        """Cancelar el contrato."""
        for record in self:
            if record.state == 'completed':
                raise UserError(
                    _('No se puede cancelar un contrato completado.')
                )
            record.state = 'cancelled'
            record.message_post(body=_('Contrato cancelado.'))

    def action_view_progress(self):
        """Devuelve una acción de ventana para ver los avances de este subcontrato."""
        self.ensure_one()

        # Obtenemos la vista de árbol (tree) y de formulario (form)
        view_tree_id = self.env.ref(
            'construction_subcontracts.view_work_progress_tree').id
        view_form_id = self.env.ref(
            'construction_subcontracts.view_work_progress_form').id

        return {
            'name': _('Avances de Obra (%s)') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'construction.work.progress',
            'views': [(view_tree_id, 'tree'), (view_form_id, 'form')],
            'domain': [('subcontract_id', '=', self.id)],
            'context': {
                'default_subcontract_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_unit_price': self.unit_price,
                'default_measurement_unit': self.measurement_unit,
                'default_guarantee_percentage': self.guarantee_percentage,
            },
        }

    def action_release_guarantee_wizard(self):
        """Devuelve una acción para abrir el asistente de liberación de garantía."""
        self.ensure_one()
        if self.state != 'completed':
            raise UserError(
                _('Solo se puede liberar la garantía de contratos completados.')
            )

        if self.total_guarantee_retained <= 0:
            raise UserError(
                _('No hay garantía retenida pendiente de liberación.')
            )

        # Utilizamos el wizard que definiremos más adelante
        return {
            'name': _('Liberar Garantía Retenida'),
            'type': 'ir.actions.act_window',
            'res_model': 'release.guarantee.wizard',  # Modelo del wizard
            'view_mode': 'form',
            'context': {
                'default_subcontract_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_amount_retained': self.total_guarantee_retained,
            },
            'target': 'new',  # Abre como ventana modal
        }

    # ============================
    # ELIMINACIÓN
    # ============================
    def unlink(self):
        """Restricción: No permitir eliminar contratos activos o completados."""
        if any(self.filtered(lambda s: s.state in ('active', 'completed'))):
            raise UserError(
                _('No puedes eliminar un subcontrato que está Activo o Completado. Cámbialo a Cancelado primero.')
            )
        return super().unlink()
