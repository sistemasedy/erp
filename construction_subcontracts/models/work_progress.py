from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionWorkProgress(models.Model):
    _name = 'construction.work.progress'
    _description = 'Avance de Obra'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    # ============================
    # CAMPOS BÁSICOS
    # ============================
    name = fields.Char(
        string='Referencia',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nuevo')
    )

    subcontract_id = fields.Many2one(
        comodel_name='construction.subcontract',
        string='Subcontrato',
        required=True,
        ondelete='cascade',
        tracking=True
    )

    partner_id = fields.Many2one(
        related='subcontract_id.partner_id',
        string='Ajustero',
        store=True
    )

    project_id = fields.Many2one(
        related='subcontract_id.project_id',
        string='Proyecto',
        store=True
    )

    date = fields.Date(
        string='Fecha del Avance',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )

    # ============================
    # CAMPOS DE MEDICIÓN
    # ============================
    measurement_unit = fields.Char(  # <-- Cambiado a Char para coincidir
        related='subcontract_id.measurement_unit',
        string='Unidad',
        readonly=True,  # Recomendado para campos 'related' simples
        store=True
    )

    unit_price = fields.Monetary(
        related='subcontract_id.unit_price',
        string='Precio Unitario',
        store=True
    )

    quantity_done = fields.Float(
        string='Cantidad Ejecutada',
        required=True,
        help='Cantidad medida en esta semana'
    )

    amount = fields.Monetary(
        string='Monto',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )

    guarantee_percentage = fields.Float(
        related='subcontract_id.guarantee_percentage',
        string='% Garantía',
        store=True
    )

    guarantee_amount = fields.Monetary(
        string='Monto Garantía Retenida',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )

    net_payment = fields.Monetary(
        string='Pago Neto (sin garantía)',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id',
        help='Monto que se pagará esta semana'
    )

    currency_id = fields.Many2one(
        related='subcontract_id.currency_id'
    )

    # ============================
    # CAMPOS DE VALIDACIÓN
    # ============================
    description = fields.Text(
        string='Descripción del Avance',
        help='Ej: Instalación andamios Nivel 5, área norte'
    )

    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string='Fotos/Documentos',
        help='Fotos del avance para validación'
    )

    validated_by = fields.Many2one(
        comodel_name='res.users',
        string='Validado Por',
        readonly=True,
        tracking=True
    )

    validation_date = fields.Datetime(
        string='Fecha Validación',
        readonly=True
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('pending', 'Pendiente Validación'),
            ('validated', 'Validado'),
            ('rejected', 'Rechazado'),
        ],
        string='Estado',
        default='draft',
        required=True,
        tracking=True
    )

    rejection_reason = fields.Text(
        string='Motivo de Rechazo'
    )

    # ============================
    # CAMPOS DE FACTURACIÓN
    # ============================
    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='Factura Generada',
        readonly=True,
        copy=False
    )

    invoice_state = fields.Selection(
        related='invoice_id.state',
        string='Estado Factura'
    )

    # ============================
    # MÉTODOS COMPUTE
    # ============================
    @api.depends('quantity_done', 'unit_price', 'guarantee_percentage')
    def _compute_amounts(self):
        for record in self:
            record.amount = record.quantity_done * record.unit_price
            record.guarantee_amount = record.amount * \
                (record.guarantee_percentage / 100)
            record.net_payment = record.amount - record.guarantee_amount

    # ============================
    # VALIDACIONES
    # ============================
    @api.constrains('quantity_done')
    def _check_quantity_done(self):
        for record in self:
            if record.quantity_done <= 0:
                raise ValidationError(
                    _('La cantidad ejecutada debe ser mayor a cero.')
                )

    @api.constrains('subcontract_id', 'quantity_done')
    def _check_total_quantity(self):
        """Verificar que no se exceda la cantidad del contrato"""
        for record in self:
            if record.state == 'validated':
                total = record.subcontract_id.total_quantity_done
                if total > record.subcontract_id.estimated_quantity * 1.1:  # 10% tolerancia
                    raise ValidationError(
                        _('ADVERTENCIA: La cantidad total ejecutada (%.2f) '
                          'excede en más del 10%% lo estimado en el contrato (%.2f).') % (
                            total,
                            record.subcontract_id.estimated_quantity
                        )
                    )

    # ============================
    # MÉTODOS DE NEGOCIO
    # ============================
    @api.model
    def create(self, vals):
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.work.progress'
            ) or _('Nuevo')
        return super().create(vals)

    def action_submit(self):
        """Enviar para validación al ingeniero"""
        for record in self:
            if record.state != 'draft':
                raise UserError(
                    _('Solo se pueden enviar avances en borrador.'))
            record.state = 'pending'

            # Notificar al ingeniero (usuario con grupo específico)
            engineer_users = self.env.ref(
                'construction_subcontracts.group_construction_engineer'
            ).users
            record.message_post(
                body=_('Nuevo avance pendiente de validación: %.2f %s') % (
                    record.quantity_done,
                    dict(record._fields['measurement_unit'].selection).get(
                        record.measurement_unit
                    )
                ),
                partner_ids=engineer_users.mapped('partner_id').ids
            )

    def action_validate(self):
        """Validar avance y generar cuenta por pagar"""
        for record in self:
            if record.state != 'pending':
                raise UserError(
                    _('Solo se pueden validar avances pendientes.')
                )

            record.write({
                'state': 'validated',
                'validated_by': self.env.user.id,
                'validation_date': fields.Datetime.now(),
            })

            # Generar factura de proveedor (cuenta por pagar)
            record._create_vendor_bill()

    def action_reject(self):
        """Rechazar avance"""
        return {
            'name': _('Rechazar Avance'),
            'type': 'ir.actions.act_window',
            'res_model': 'construction.work.progress',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'show_rejection_reason': True},
        }

    def _create_vendor_bill(self):
        """Crear factura de proveedor con retención de garantía"""
        self.ensure_one()

        AccountMove = self.env['account.move']
        invoice_vals = {
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': self.date,
            'invoice_line_ids': [(0, 0, {
                'name': f'{self.subcontract_id.work_description} - Avance {self.name}',
                'quantity': self.quantity_done,
                'price_unit': self.unit_price,
                'analytic_distribution': {
                    self.project_id.analytic_account_id.id: 100
                } if self.project_id.analytic_account_id else False,
            })],
            'narration': f'Garantía retenida: {self.guarantee_amount:.2f} '
            f'({self.guarantee_percentage}%)',
        }

        invoice = AccountMove.create(invoice_vals)
        self.invoice_id = invoice.id

        return invoice
