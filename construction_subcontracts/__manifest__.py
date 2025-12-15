# -*- coding: utf-8 -*-
{
    'name': 'Gestión de Subcontratos y Cubicaciones',
    'version': '17.0.1.0.0',
    'category': 'Construction',
    'sequence': 10,
    'summary': 'Control de pagos por avance de obra para constructoras',
    'description': """
Gestión de Subcontratos para Construcción
==========================================

Módulo especializado para empresas de construcción que trabajan con
subcontratistas (ajusteros). Permite:

Características Principales:
----------------------------
* Contratos con precios unitarios (m², ml, m³, unidades)
* Registro de avances semanales con validación
* Cálculo automático de cuentas por pagar
* Retención de garantía configurable (default 20%)
* Integración completa con contabilidad y proyectos
* Flujo de aprobación: Capataz → Ingeniero → Contabilidad
* Auditoría completa de cambios
* Reportes para DGII (República Dominicana)

Flujo de Trabajo:
-----------------
1. Se crea un subcontrato con precio unitario y cantidad estimada
2. El capataz registra avances semanales desde tablet
3. El ingeniero valida el avance con fotos adjuntas
4. Se genera automáticamente la factura con retención de garantía
5. La contadora procesa el pago
6. Al finalizar la obra, el gerente libera la garantía retenida

Roles y Permisos:
-----------------
* Capataz: Registra avances de SU proyecto
* Ingeniero: Valida avances y crea contratos
* Gerente: Acceso total y liberación de garantías
* Contadora: Gestión de pagos y reportes

    """,
    'author': 'Construcciones Lamout S.R.L.',
    'website': 'https://www.construccioneslamout.com',
    'license': 'LGPL-3',

    # Dependencias
    'depends': [
        'base',
        'mail',               # Para chatter y notificaciones
        'account',            # Contabilidad
        'project',            # Gestión de proyectos
        'purchase',           # Órdenes de compra
        'hr',                 # Recursos humanos (opcional)
        'l10n_do',
        'uom',
        # Localización Dominicana (NCF, DGII)
    ],

    # Archivos de datos (SE CARGAN EN ESTE ORDEN)
    # En construction_subcontracts/__manifest__.py
    'data': [
        # 1. SEGURIDAD BASE (Grupos y Reglas de Acceso por registro)
        'security/security.xml',              # GRUPOS y ROLES (res.groups)

        # 2. DATOS MAESTROS Y SECUENCIAS
        'data/sequences.xml',                 # Numeración automática
        'data/measurement_units.xml',         # Unidades de medida

        # A PARTIR DE AQUÍ, LOS MODELOS PYTHON DEBEN ESTAR CARGADOS.

        # 3. REGLAS DE ACCESO (Permisos de Modelo y Campo)
        # Recomendación: Mover los registros 'ir.model.fields' de security.xml a este archivo.
        'security/ir.model.access.csv',       # Permisos CRUD (ir.model.access)

        # 4. VISTAS
        'views/subcontract_views.xml',
        'views/work_progress_views.xml',
        'views/guarantee_retention_views.xml',  # Asumo que este archivo existe
        'views/menu.xml',
        # ...
    ],

    # Archivos de demostración (solo se cargan si demo=True al crear BD)
    'demo': [
        'demo/demo_partners.xml',
        'demo/demo_projects.xml',
        'demo/demo_subcontracts.xml',
    ],

    # Assets (CSS, JS)
    'assets': {
        'web.assets_backend': [
            'construction_subcontracts/static/src/css/subcontracts.css',
            'construction_subcontracts/static/src/js/subcontracts.js',
        ],
    },

    # Imágenes
    'images': [
        'static/description/banner.jpeg',
        'static/description/icon.jpeg',
    ],

    # Configuración del módulo
    'installable': True,
    'application': True,              # Es una aplicación independiente
    'auto_install': False,            # No se instala automáticamente
    'price': 0.00,
    # 'currency': 'USD',

    # Post-instalación
    # 'post_init_hook': 'post_init_hook',
}
