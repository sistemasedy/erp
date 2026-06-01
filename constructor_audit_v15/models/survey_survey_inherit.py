from odoo import models, fields


class SurveySurveyAudit(models.Model):
    _inherit = 'survey.survey'

    x_is_audit_survey = fields.Boolean(
        string='Es Survey de Constructor Audit',
        default=False,
        help='Activa el pipeline automático de diagnóstico al completarse este cuestionario.'
    )