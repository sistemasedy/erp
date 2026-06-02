from odoo import models, fields, api
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class SurveyUserInputAudit(models.Model):
    _inherit = 'survey.user_input'

    # ── Datos financieros capturados en el Survey ─────────────────────────
    # Estos campos se pueblan desde las preguntas de tipo "número"
    # cuyo question_code coincide con el campo correspondiente.
    x_audit_facturacion      = fields.Float('Facturación Anual (USD)', default=0.0)
    x_audit_pct_materiales   = fields.Float('% Gasto en Materiales',   default=45.0)
    x_audit_num_subcontratas = fields.Float('Nº Subcontratistas/Obra', default=5.0)
    x_audit_duracion_meses   = fields.Float('Duración Promedio Obra (meses)', default=6.0)
    x_audit_num_proyectos    = fields.Float('Nº Proyectos Simultáneos', default=3.0)
    x_audit_costo_hora       = fields.Float('Costo Hora Equipo (USD)',  default=25.0)

    # ── Resultado calculado ───────────────────────────────────────────────
    x_audit_nivel_resultado  = fields.Char('Nivel Calculado', readonly=True)
    x_audit_roi_calculado    = fields.Float('ROI Calculado', readonly=True)
    x_audit_procesado        = fields.Boolean('Diagnóstico Procesado', default=False)

    # ─────────────────────────────────────────────────────────────────────
    # Lectura automática de respuestas numéricas al guardar líneas
    # ─────────────────────────────────────────────────────────────────────

    FINANCIAL_QUESTION_CODES = {
        'facturacion_anual':    'x_audit_facturacion',
        'pct_materiales':       'x_audit_pct_materiales',
        'num_subcontratistas':  'x_audit_num_subcontratas',
        'duracion_obra_meses':  'x_audit_duracion_meses',
        'proyectos_simultaneos': 'x_audit_num_proyectos',
        'costo_hora_equipo':    'x_audit_costo_hora',
    }

    def _sync_financial_fields(self):
        """Lee las respuestas numéricas del survey y las mapea a los campos x_audit_*."""
        for record in self:
            vals = {}
            for line in record.user_input_line_ids:
                code = line.question_id.question_code
                field = self.FINANCIAL_QUESTION_CODES.get(code)
                if field and line.value_numerical_box is not None:
                    vals[field] = line.value_numerical_box
            if vals:
                record.write(vals)

    # ─────────────────────────────────────────────────────────────────────
    # Hook al completar el Survey
    # ─────────────────────────────────────────────────────────────────────

    def _mark_done(self):
        """Override: al marcar done, disparar el pipeline de diagnóstico."""
        res = super()._mark_done()
        audit_surveys = self.filtered(
            lambda r: r.survey_id.x_is_audit_survey and not r.x_audit_procesado
        )
        if audit_surveys:
            audit_surveys._sync_financial_fields()
            audit_surveys._process_audit_pipeline()
        return res

    def _process_audit_pipeline(self):
        """Orquesta: calcula score → crea lead → agenda actividad → envía email."""
        for record in self:
            try:
                score = record.scoring_percentage or 0.0

                # 1. Clasificar nivel
                if score <= 35:
                    nivel = 'principiante'
                elif score <= 69:
                    nivel = 'intermedio'
                else:
                    nivel = 'avanzado'

                # 2. Calcular ROI
                roi = self.env['audit.config'].calcular_roi(record, nivel)

                # 3. Crear/actualizar lead en CRM
                lead = self._create_or_update_lead(record, nivel, score, roi)

                # 4. Asignar etiquetas CRM
                self._assign_crm_tags(lead, nivel)

                # 5. Programar actividad para el vendedor
                self._schedule_call_activity(lead, nivel, score, roi)

                # 6. Enviar email personalizado
                self._send_level_email(record, nivel)

                # Marcar como procesado
                record.write({
                    'x_audit_nivel_resultado': nivel,
                    'x_audit_roi_calculado':   roi['total'],
                    'x_audit_procesado':       True,
                })

                _logger.info(
                    '[Constructor Audit] Pipeline completado: partner=%s, score=%s, nivel=%s, roi=$%s',
                    record.partner_id.name, score, nivel, roi['total']
                )

            except Exception as e:
                _logger.error(
                    '[Constructor Audit] Error procesando diagnóstico id=%s: %s',
                    record.id, str(e)
                )

    def _create_or_update_lead(self, record, nivel, score, roi):
        """Crea un nuevo lead o actualiza uno existente para este partner."""
        partner = record.partner_id
        Lead = self.env['crm.lead']

        # Buscar stage de entrada para leads de diagnóstico
        stage = self.env['crm.stage'].search(
            [('name', 'ilike', 'Nuevo')], limit=1
        ) or self.env['crm.stage'].search([], limit=1, order='sequence asc')

        vals = {
            'name':                  f'Diagnóstico Constructor Audit – {partner.name}',
            'partner_id':            partner.id,
            'email_from':            partner.email or '',
            'phone':                 partner.phone or '',
            'stage_id':              stage.id if stage else False,
            'x_audit_date':          fields.Datetime.now(),
            'x_audit_score':         int(score),
            'x_audit_nivel':         nivel,
            'x_audit_roi_total':     roi['total'],
            'x_audit_payback_meses': roi['payback_meses'] or 0.0,
            'x_audit_top_oportunidad': roi['top_categoria'],
            'x_audit_facturacion':   record.x_audit_facturacion,
            'x_audit_survey_url':    f'/web#id={record.id}&model=survey.user_input',
            'description': (
                f"📊 Score Constructor Audit: {int(score)}/100 | Nivel: {nivel.capitalize()}\n"
                f"💰 ROI Estimado: ${roi['total']:,} USD/año\n"
                f"⏱ Payback Odoo: {roi['payback_meses']} meses\n"
                f"🎯 Área de mayor pérdida: {roi['top_categoria']}\n\n"
                f"Desglose ROI:\n{roi['desglose_texto']}"
            ),
        }

        # Si ya existe un lead de diagnóstico para este partner, actualizarlo
        existing = Lead.search(
            [('partner_id', '=', partner.id), ('x_audit_score', '!=', False)],
            limit=1, order='id desc'
        )
        if existing:
            existing.write(vals)
            return existing

        return Lead.create(vals)

    def _assign_crm_tags(self, lead, nivel):
        """Asigna la etiqueta de nivel al lead."""
        tag_xmlids = {
            'principiante': 'constructor_audit_v15.tag_audit_principiante',
            'intermedio':   'constructor_audit_v15.tag_audit_intermedio',
            'avanzado':     'constructor_audit_v15.tag_audit_avanzado',
        }
        tag = self.env.ref(tag_xmlids[nivel], raise_if_not_found=False)
        if tag:
            lead.tag_ids = [(4, tag.id)]

    def _schedule_call_activity(self, lead, nivel, score, roi):
        """Programa actividad de llamada para el vendedor responsable."""
        labels = {
            'principiante': 'Llamada urgente',
            'intermedio':   'Llamada de cualificación',
            'avanzado':     'Llamada de propuesta Enterprise',
        }
        activity_type = self.env.ref(
            'mail.mail_activity_data_call', raise_if_not_found=False
        )
        if activity_type:
            lead.activity_schedule(
                activity_type_id=activity_type.id,
                summary=f'{labels[nivel]} – Score {int(score)} ({nivel.capitalize()})',
                note=(
                    f'Revisar diagnóstico antes de llamar.\n'
                    f'ROI estimado: ${roi["total"]:,} USD | '
                    f'Payback: {roi["payback_meses"]} meses\n'
                    f'Área crítica: {roi["top_categoria"]}'
                ),
                date_deadline=fields.Date.today() + timedelta(days=1),
            )

    def _send_level_email(self, record, nivel):
        """Envía la plantilla de email correspondiente al nivel."""
        template_xmlids = {
            'principiante': 'constructor_audit_v15.email_tpl_principiante',
            'intermedio':   'constructor_audit_v15.email_tpl_intermedio',
            'avanzado':     'constructor_audit_v15.email_tpl_avanzado',
        }
        template = self.env.ref(template_xmlids[nivel], raise_if_not_found=False)
        if template and record.partner_id.email:
            template.send_mail(record.id, force_send=True)
