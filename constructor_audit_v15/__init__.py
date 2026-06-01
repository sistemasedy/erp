from . import models
from odoo import api, SUPERUSER_ID


def post_init_hook(env):
    """Crea la configuración de benchmarks por defecto al instalar."""
    AuditConfig = env['audit.config']
    if not AuditConfig.search([], limit=1):
        AuditConfig.create({
            'name': 'Benchmarks por Defecto (LatAm/RD)',
            'desperdicio_principiante': 15.0,
            'desperdicio_intermedio': 8.0,
            'desperdicio_avanzado': 3.0,
            'sobrepago_principiante': 20.0,
            'sobrepago_intermedio': 12.0,
            'sobrepago_avanzado': 5.0,
            'retraso_principiante': 3.5,
            'retraso_intermedio': 1.8,
            'retraso_avanzado': 0.8,
            'horas_perd_principiante': 20.0,
            'horas_perd_intermedio': 12.0,
            'horas_perd_avanzado': 4.0,
            'costo_odoo_principiante': 3500.0,
            'costo_odoo_intermedio': 6500.0,
            'costo_odoo_avanzado': 12000.0,
        })
