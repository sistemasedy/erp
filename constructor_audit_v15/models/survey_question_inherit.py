from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_code = fields.Char(
        string='Código de Pregunta',
        index=True,
        help='Código único para identificar preguntas en el motor de diagnóstico.',
    )
