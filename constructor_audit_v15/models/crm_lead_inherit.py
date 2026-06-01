from odoo import models, fields, api


class CrmLeadAudit(models.Model):
    _inherit = 'crm.lead'

    # ── Campos base del diagnóstico ───────────────────────────────────────
    x_audit_score           = fields.Integer(string='Score de Eficiencia', readonly=True)
    x_audit_nivel           = fields.Selection(
        selection=[
            ('principiante', 'Principiante (Manual)'),
            ('intermedio',   'Intermedio (Desconectado)'),
            ('avanzado',     'Avanzado (Optimizado)'),
        ],
        string='Nivel de Madurez', readonly=True,
    )
    x_audit_roi_total       = fields.Float(string='ROI Estimado (USD/año)', readonly=True, digits=(16, 2))
    x_audit_payback_meses   = fields.Float(string='Payback Odoo (meses)', readonly=True, digits=(5, 1))
    x_audit_top_oportunidad = fields.Char(string='Área de Mayor Pérdida', readonly=True)
    x_audit_facturacion     = fields.Float(string='Facturación Anual (USD)', readonly=True, digits=(16, 2))
    x_audit_survey_url      = fields.Char(string='URL del Diagnóstico', readonly=True)

    # ── Campos nuevos (faltaban en la vista) ──────────────────────────────
    x_audit_date = fields.Datetime(
        string='Fecha del Diagnóstico', readonly=True,
    )
    x_audit_monthly_loss = fields.Float(
        string='Pérdida Mensual (USD)', readonly=True, digits=(16, 2),
        compute='_compute_monthly_loss', store=True,
    )
    x_audit_priority = fields.Selection(
        selection=[
            ('low',      'Baja'),
            ('medium',   'Media'),
            ('high',     'Alta'),
            ('critical', 'Crítica'),
        ],
        string='Prioridad de Intervención', readonly=True,
        compute='_compute_priority', store=True,
    )
    x_audit_recommendation = fields.Text(
        string='Recomendación Principal', readonly=True,
    )

    @api.depends('x_audit_roi_total')
    def _compute_monthly_loss(self):
        for rec in self:
            rec.x_audit_monthly_loss = round(
                rec.x_audit_roi_total / 12.0, 2
            ) if rec.x_audit_roi_total else 0.0

    @api.depends('x_audit_score')
    def _compute_priority(self):
        for rec in self:
            score = rec.x_audit_score or 0
            if score <= 20:
                rec.x_audit_priority = 'critical'
            elif score <= 40:
                rec.x_audit_priority = 'high'
            elif score <= 65:
                rec.x_audit_priority = 'medium'
            else:
                rec.x_audit_priority = 'low'
