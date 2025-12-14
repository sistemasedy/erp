from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionSubcontract(models.Model):
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
        tracking=True
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
        string='Moneda'
    )

    # ============================
    # CAMPOS DE CONTRATO
    # ============================
    work_description = fields.Text(
        string='Descripción del Trabajo',
        required=True,
        help='Ej: Instalación de andamios en Torre Nivel 3-7'
    )

    measurement_unit = fields.Selection(
        selection=[
            ('m2', 'Metro Cuadrado (m²)'),
            ('ml', 'Metro Lineal (ml)'),
            ('m3', 'Metro Cúbico (m³)'),
            ('unit', 'Unidad'),
            ('kg', 'Kilogramo'),
            ('ton', 'Tonelada'),
        ],
        string='Unidad de Medida',
        required=True,
        default='m2'
    )

    unit_price = fields.Monetary(
        string='Precio Unitario',
        required=True,
        currency_field='currency_id',
        help='Precio por cada unidad de medida'
    )

    estimated_quantity = fields.Float(
        string='Cantidad Estimada',
        required=True,
        help='Cantidad total estimada del contrato'
    )

    contract_amount = fields.Monetary(
        string='Monto Total Contrato',
        compute='_compute_contract_amount',
        store=True,
        currency_field='currency_id'
    )

    guarantee_percentage = fields.Float(
        string='% Retención de Garantía',
        default=20.0,
        required=True,
        help='Porcentaje que se retiene hasta finalizar la obra (típicamente 20%)'
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
        string='Avances de Obra'
    )

    total_quantity_done = fields.Float(
        string='Cantidad Total Ejecutada',
        compute='_compute_totals',
        store=True
    )

    total_amount_invoiced = fields.Monetary(
        string='Total Facturado',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id'
    )

    total_guarantee_retained = fields.Monetary(
        string='Total Garantía Retenida',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id'
    )

    total_paid = fields.Monetary(
        string='Total Pagado (sin garantía)',
        compute='_compute_totals',
        store=True,
        currency_field='currency_id'
    )

    percentage_completed = fields.Float(
        string='% Completado',
        compute='_compute_percentage',
        store=True
    )

    # ============================
    # CAMPOS DE ESTADO
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

    notes = fields.Html(string='Notas')

    # ============================
    # MÉTODOS COMPUTE
    # ============================
    @api.depends('unit_price', 'estimated_quantity')
    def _compute_contract_amount(self):
        for record in self:
            record.contract_amount = record.unit_price * record.estimated_quantity

    @api.depends('progress_ids.quantity_done', 'progress_ids.amount',
                 'progress_ids.guarantee_amount', 'progress_ids.state')
    def _compute_totals(self):
        for record in self:
            validated_progress = record.progress_ids.filtered(
                lambda p: p.state == 'validated'
            )
            record.total_quantity_done = sum(
                validated_progress.mapped('quantity_done'))
            record.total_amount_invoiced = sum(
                validated_progress.mapped('amount'))
            record.total_guarantee_retained = sum(
                validated_progress.mapped('guarantee_amount'))
            record.total_paid = record.total_amount_invoiced - record.total_guarantee_retained

    @api.depends('total_quantity_done', 'estimated_quantity')
    def _compute_percentage(self):
        for record in self:
            if record.estimated_quantity > 0:
                record.percentage_completed = (
                    record.total_quantity_done / record.estimated_quantity
                ) * 100
            else:
                record.percentage_completed = 0.0

    # ============================
    # VALIDACIONES
    # ============================
    @api.constrains('unit_price')
    def _check_unit_price(self):
        for record in self:
            if record.unit_price <= 0:
                raise ValidationError(
                    _('El precio unitario debe ser mayor a cero.')
                )

    @api.constrains('estimated_quantity')
    def _check_estimated_quantity(self):
        for record in self:
            if record.estimated_quantity <= 0:
                raise ValidationError(
                    _('La cantidad estimada debe ser mayor a cero.')
                )

    @api.constrains('guarantee_percentage')
    def _check_guarantee_percentage(self):
        for record in self:
            if not (0 <= record.guarantee_percentage <= 100):
                raise ValidationError(
                    _('El porcentaje de garantía debe estar entre 0% y 100%.')
                )

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_end and record.date_start > record.date_end:
                raise ValidationError(
                    _('La fecha de fin no puede ser anterior a la fecha de inicio.')
                )

    # ============================
    # MÉTODOS DE NEGOCIO
    # ============================
    @api.model
    def create(self, vals):
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.subcontract'
            ) or _('Nuevo')
        return super().create(vals)

    def action_activate(self):
        """Activar el contrato"""
        for record in self:
            if record.state != 'draft':
                raise UserError(
                    _('Solo se pueden activar contratos en borrador.'))
            record.state = 'active'
            record.message_post(
                body=_('Contrato activado por %s') % self.env.user.name
            )

    def action_complete(self):
        """Completar el contrato"""
        for record in self:
            if record.state != 'active':
                raise UserError(
                    _('Solo se pueden completar contratos activos.'))
            record.state = 'completed'
            record.message_post(
                body=_('Contrato completado. Total ejecutado: %.2f %s') % (
                    record.total_quantity_done,
                    dict(record._fields['measurement_unit'].selection).get(
                        record.measurement_unit
                    )
                )
            )

    def action_cancel(self):
        """Cancelar el contrato"""
        for record in self:
            if record.state == 'completed':
                raise UserError(
                    _('No se puede cancelar un contrato completado.')
                )
            record.state = 'cancelled'

    def action_view_progress(self):
        """Abrir vista de avances"""
        self.ensure_one()
        return {
            'name': _('Avances de Obra'),
            'type': 'ir.actions.act_window',
            'res_model': 'construction.work.progress',
            'view_mode': 'tree,form',
            'domain': [('subcontract_id', '=', self.id)],
            'context': {
                'default_subcontract_id': self.id,
                'default_unit_price': self.unit_price,
                'default_measurement_unit': self.measurement_unit,
            },
        }

    def action_release_guarantee(self):
        """Liberar garantía retenida (cuando la obra está perfecta)"""
        self.ensure_one()
        if self.state != 'completed':
            raise UserError(
                _('Solo se puede liberar garantía de contratos completados.')
            )

        # Aquí se crearía la factura/pago final con el monto de garantía
        # TODO: Implementar creación de account.move

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Garantía Liberada'),
                'message': _('Se ha liberado %.2f en garantía retenida.') % (
                    self.total_guarantee_retained
                ),
                'type': 'success',
                'sticky': False,
            }
        }
