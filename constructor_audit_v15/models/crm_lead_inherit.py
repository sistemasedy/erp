from odoo import models, fields


class CrmLeadAudit(models.Model):
    _inherit = 'crm.lead'

    # ── Campos del diagnóstico Constructor Audit ──────────────────────────
    x_audit_score          = fields.Integer(string='Score de Eficiencia', readonly=True)
    x_audit_nivel          = fields.Selection(
        selection=[
            ('principiante', 'Principiante (Manual)'),
            ('intermedio',   'Intermedio (Desconectado)'),
            ('avanzado',     'Avanzado (Optimizado)'),
        ],
        string='Nivel de Madurez',
        readonly=True,
    )
    x_audit_roi_total      = fields.Monetary(string='ROI Estimado (USD/año)', readonly=True,
                                             currency_field='company_currency')
    x_audit_payback_meses  = fields.Float(string='Payback Odoo (meses)', readonly=True, digits=(5, 1))
    x_audit_top_oportunidad = fields.Char(string='Área de Mayor Pérdida', readonly=True)
    x_audit_facturacion    = fields.Monetary(string='Facturación Anual Declarada', readonly=True,
                                             currency_field='company_currency')
    x_audit_survey_url     = fields.Char(string='URL del Diagnóstico', readonly=True)

    company_currency = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True
    )
