# -*- coding: utf-8 -*-
from odoo import models, fields, api
from pytz import timezone

class PosConfig(models.Model):
    _inherit = 'pos.config'

    default_partner_id = fields.Many2one('res.partner', string="Select Customer")
    last_session_closing_date = fields.Date(compute='_compute_last_session', store=True)
    last_session_closing_cash = fields.Float(compute='_compute_last_session', store=True)

    @api.depends('session_ids.stop_at')
    def _compute_last_session(self):
        for pos_config in self:
            # Filtrar sesiones con un valor válido de stop_at
            valid_sessions = pos_config.session_ids.filtered(lambda s: s.stop_at)
            session = valid_sessions.sorted(key=lambda s: s.stop_at, reverse=True)
            if session:
                # Obtener la zona horaria del usuario o utilizar UTC por defecto
                user_tz = self.env.user.tz or 'UTC'
                try:
                    user_tz = timezone(user_tz)
                except Exception:
                    user_tz = UTC
                pos_config.last_session_closing_date = session[0].stop_at.astimezone(user_tz).date()
                pos_config.last_session_closing_cash = session[0].cash_register_balance_end_real
            else:
                pos_config.last_session_closing_date = False
                pos_config.last_session_closing_cash = 0.0


