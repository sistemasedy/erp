from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class AuditConfig(models.Model):
    _name = 'audit.config'
    _description = 'Configuración de Benchmarks y Fórmulas ROI'
    _rec_name = 'name'

    name = fields.Char(string='Nombre', required=True, default='Benchmarks por Defecto')

    # ── Benchmarks de desperdicio en compras (%) ──────────────────────────
    desperdicio_principiante = fields.Float('Desperdicio Compras - Principiante (%)', default=15.0)
    desperdicio_intermedio   = fields.Float('Desperdicio Compras - Intermedio (%)',   default=8.0)
    desperdicio_avanzado     = fields.Float('Desperdicio Compras - Avanzado (%)',     default=3.0)

    # ── Benchmarks de sobrepago a subcontratistas (%) ─────────────────────
    sobrepago_principiante = fields.Float('Sobrepago Subcontratas - Principiante (%)', default=20.0)
    sobrepago_intermedio   = fields.Float('Sobrepago Subcontratas - Intermedio (%)',   default=12.0)
    sobrepago_avanzado     = fields.Float('Sobrepago Subcontratas - Avanzado (%)',     default=5.0)

    # ── Meses de retraso promedio por obra ────────────────────────────────
    retraso_principiante = fields.Float('Retraso Promedio - Principiante (meses)', default=3.5)
    retraso_intermedio   = fields.Float('Retraso Promedio - Intermedio (meses)',   default=1.8)
    retraso_avanzado     = fields.Float('Retraso Promedio - Avanzado (meses)',     default=0.8)

    # ── Horas administrativas perdidas por semana ─────────────────────────
    horas_perd_principiante = fields.Float('Horas Admin Perdidas/Sem - Principiante', default=20.0)
    horas_perd_intermedio   = fields.Float('Horas Admin Perdidas/Sem - Intermedio',   default=12.0)
    horas_perd_avanzado     = fields.Float('Horas Admin Perdidas/Sem - Avanzado',     default=4.0)

    # ── Costo estimado de implementación Odoo por nivel (USD) ─────────────
    costo_odoo_principiante = fields.Float('Costo Odoo - Principiante (USD)', default=3500.0)
    costo_odoo_intermedio   = fields.Float('Costo Odoo - Intermedio (USD)',   default=6500.0)
    costo_odoo_avanzado     = fields.Float('Costo Odoo - Avanzado (USD)',     default=12000.0)

    # ─────────────────────────────────────────────────────────────────────
    # Motor de cálculo ROI
    # ─────────────────────────────────────────────────────────────────────

    @api.model
    def get_active_config(self):
        config = self.search([], limit=1, order='id asc')
        if not config:
            config = self.create({'name': 'Benchmarks por Defecto'})
        return config

    @api.model
    def calcular_roi(self, survey_input, nivel):
        """
        Calcula el ROI potencial anual basado en las respuestas del Survey
        y los benchmarks configurados.

        Args:
            survey_input: record de survey.user_input
            nivel: 'principiante' | 'intermedio' | 'avanzado'

        Returns:
            dict con total, desglose, payback_meses, top_categoria, etc.
        """
        cfg = self.get_active_config()

        # ── Leer datos financieros del Survey ────────────────────────────
        facturacion    = survey_input.x_audit_facturacion    or 300000.0
        pct_materiales = (survey_input.x_audit_pct_materiales or 45.0) / 100.0
        n_subcontratas = survey_input.x_audit_num_subcontratas or 5.0
        dur_meses      = survey_input.x_audit_duracion_meses  or 6.0
        n_proyectos    = survey_input.x_audit_num_proyectos   or 3.0
        costo_hora     = survey_input.x_audit_costo_hora      or 25.0

        # ── Seleccionar factores según nivel ─────────────────────────────
        factores = {
            'principiante': {
                'desperdicio': cfg.desperdicio_principiante / 100.0,
                'sobrepago':   cfg.sobrepago_principiante   / 100.0,
                'retraso':     cfg.retraso_principiante,
                'horas_perd':  cfg.horas_perd_principiante,
                'costo_odoo':  cfg.costo_odoo_principiante,
            },
            'intermedio': {
                'desperdicio': cfg.desperdicio_intermedio / 100.0,
                'sobrepago':   cfg.sobrepago_intermedio   / 100.0,
                'retraso':     cfg.retraso_intermedio,
                'horas_perd':  cfg.horas_perd_intermedio,
                'costo_odoo':  cfg.costo_odoo_intermedio,
            },
            'avanzado': {
                'desperdicio': cfg.desperdicio_avanzado / 100.0,
                'sobrepago':   cfg.sobrepago_avanzado   / 100.0,
                'retraso':     cfg.retraso_avanzado,
                'horas_perd':  cfg.horas_perd_avanzado,
                'costo_odoo':  cfg.costo_odoo_avanzado,
            },
        }
        f = factores.get(nivel, factores['intermedio'])

        obras_anuales = max(1.0, round(12.0 / max(dur_meses, 1)) * n_proyectos)

        # ── 1. Ahorro en Compras ──────────────────────────────────────────
        gasto_mat      = facturacion * pct_materiales
        ahorro_compras = gasto_mat * f['desperdicio'] * 0.85

        # ── 2. Ahorro en Subcontratistas ──────────────────────────────────
        pago_sub_obra     = (facturacion * 0.35) / max(n_proyectos, 1)
        ahorro_subcontratas = n_subcontratas * pago_sub_obra * f['sobrepago'] * obras_anuales

        # ── 3. Ahorro por Reducción de Retrasos ───────────────────────────
        costo_fijo_mes  = facturacion * 0.10 / 12.0
        ahorro_retrasos = costo_fijo_mes * f['retraso'] * 0.70 * n_proyectos

        # ── 4. Ahorro Administrativo ──────────────────────────────────────
        ahorro_admin = f['horas_perd'] * costo_hora * 52.0 * 0.80

        total = ahorro_compras + ahorro_subcontratas + ahorro_retrasos + ahorro_admin

        payback = round(f['costo_odoo'] / (total / 12.0), 1) if total > 0 else None

        categorias = {
            'Compras y materiales': ahorro_compras,
            'Subcontratistas':      ahorro_subcontratas,
            'Retrasos en obra':     ahorro_retrasos,
            'Gestión administrativa': ahorro_admin,
        }
        top_categoria = max(categorias, key=categorias.get)

        desglose_texto = '\n'.join(
            f'  • {k}: ${round(v):,}' for k, v in categorias.items()
        )

        _logger.info(
            '[Constructor Audit] ROI calculado para nivel=%s: total=$%s, payback=%s meses',
            nivel, round(total), payback
        )

        return {
            'total':          round(total),
            'desglose':       {k: round(v) for k, v in categorias.items()},
            'desglose_texto': desglose_texto,
            'payback_meses':  payback,
            'top_categoria':  top_categoria,
            'costo_odoo':     f['costo_odoo'],
            'roi_porcentaje': round((total / f['costo_odoo']) * 100) if f['costo_odoo'] else 0,
        }
