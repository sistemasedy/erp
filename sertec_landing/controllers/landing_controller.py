# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

IDEMPOTENCY_WINDOW_MINUTES = 10
SOURCE_TAG   = "Landing Page - Edy Mejía"
DEFAULT_ZONE = "No especificada"


def _ok(message, **kwargs):
    result = {"status": "success", "message": message}
    result.update(kwargs)
    return result


def _err(message, code="GENERIC_ERROR"):
    return {"status": "error", "code": code, "message": message}


class LandingPageController(http.Controller):

    @http.route('/landing', type='http', auth='public', website=True)
    def render_landing_page(self, **kw):
        return request.render('sertec_landing.edy_mejia_landing_template')

    @http.route(
        '/api/lead/create',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False,
        cors='*',
    )
    def create_lead_from_landing(self, **kwargs):
        try:
            data   = request.jsonrequest or {}
            params = data.get('params', data)

            name  = (params.get('name')  or '').strip()
            phone = (params.get('phone') or '').strip()
            zone  = (params.get('zone')  or DEFAULT_ZONE).strip()

            if not name:
                return _err("El nombre es obligatorio.", code="MISSING_NAME")
            if not phone:
                return _err("El teléfono / WhatsApp es obligatorio.", code="MISSING_PHONE")
            if len(phone.replace(' ', '').replace('-', '')) < 7:
                return _err("Número de teléfono inválido.", code="INVALID_PHONE")

            threshold = datetime.now() - timedelta(minutes=IDEMPOTENCY_WINDOW_MINUTES)
            existing = request.env['crm.lead'].sudo().search([
                ('phone', '=', phone),
                ('create_date', '>=', threshold.strftime('%Y-%m-%d %H:%M:%S')),
            ], limit=1)

            if existing:
                _logger.info(
                    "[landing_crm] Duplicado | phone=%s | lead_id=%s",
                    phone, existing.id
                )
                return _ok(
                    "Registro ya procesado anteriormente.",
                    lead_id=existing.id,
                    duplicate=True,
                )

            stage = request.env['crm.stage'].sudo().search(
                [], order='sequence asc', limit=1
            )

            tag = request.env['crm.tag'].sudo().search(
                [('name', '=', SOURCE_TAG)], limit=1
            )
            if not tag:
                tag = request.env['crm.tag'].sudo().create({'name': SOURCE_TAG})

            lead_vals = {
                'name': "Interés Landing: " + name + " — " + zone,
                'contact_name': name,
                'phone': phone,
                'description': (
                    "Lead capturado desde Landing Page de Consultoría.\n"
                    "Zona de interés: " + zone + "\n"
                    "Fuente: " + SOURCE_TAG
                ),
                'type': 'lead',
                'tag_ids': [(4, tag.id)],
            }
            if stage:
                lead_vals['stage_id'] = stage.id

            new_lead = request.env['crm.lead'].sudo().create(lead_vals)

            _logger.info(
                "[landing_crm] Lead creado | id=%s | name=%s | phone=%s | zone=%s",
                new_lead.id, name, phone, zone,
            )

            return _ok("Lead creado correctamente.", lead_id=new_lead.id)

        except Exception as exc:
            _logger.exception(
                "[landing_crm] Error crítico: %s", exc
            )
            return _err(
                "Error interno en el servidor. Por favor intenta de nuevo.",
                code="INTERNAL_ERROR",
            )

    @http.route(
        '/api/lead/ping',
        type='json',
        auth='public',
        methods=['GET', 'POST'],
        csrf=False,
        cors='*',
    )
    def ping(self, **kwargs):
        return {
            "status": "ok",
            "module": "sertec_landing",
            "version": "15.0.1.0.0",
        }
