# 🛠️ Gestión de Subcontratos y Cubicaciones (construction_subcontracts)

Este módulo está diseñado específicamente para empresas de construcción que trabajan con subcontratistas (ajusteros) y necesitan un control riguroso de los avances de obra, las cubicaciones y la gestión de retenciones de garantía.

## 🌟 Características Principales

* **Subcontratos Detallados:** Gestión de contratos con precios unitarios (m², ml, m³, unidades) vinculados a proyectos y tareas específicas.
* **Registro de Avances (Cubicaciones):** Permite el registro detallado y cronológico de los avances semanales o por etapa por parte del personal de campo.
* **Flujo de Aprobación:** Implementa un flujo de validación de tres etapas: **Capataz** (Registro) → **Ingeniero** (Validación con adjuntos) → **Contabilidad** (Procesamiento de Pago).
* **Gestión de Retenciones:** Cálculo automático y transparente de la Retención de Garantía configurable (ej: 20%), liberable al finalizar la obra mediante un asistente dedicado.
* **Integración Contable:** Generación automática de facturas de proveedor (cuentas por pagar) con las retenciones aplicadas, asegurando la correcta contabilidad del pasivo.
* **Localización:** Soporte e integración para requisitos fiscales locales (e.g., NCF y reportes DGII en República Dominicana).

## 🚀 Flujo de Trabajo

1.  **Creación del Subcontrato:** El Ingeniero crea un Subcontrato vinculado a un proyecto, con el subcontratista, la unidad de medida, el precio unitario y la cantidad total estimada.
2.  **Registro de Avance (Cubicación):** El Capataz registra los avances de obra (cantidad ejecutada) semanalmente o según la periodicidad definida.
3.  **Validación del Ingeniero:** El Ingeniero revisa el avance, adjunta evidencias fotográficas/documentales y lo aprueba.
4.  **Generación de Factura:** Una vez aprobado, el sistema genera automáticamente una factura de proveedor que refleja el monto a pagar *menos* la retención de garantía.
5.  **Procesamiento de Pago:** La Contadora procesa el pago de la factura. La Retención de Garantía queda registrada como un pasivo hasta la finalización.
6.  **Liberación de Garantía:** Al terminar la obra, el Gerente o Administrador utiliza el **Asistente de Liberación de Garantía** para generar la factura final por el monto retenido y procesar el pago.

## 👥 Roles y Permisos

| Rol | Responsabilidad Principal | Permisos |
| :--- | :--- | :--- |
| **Capataz** | Registro de avances de obra. | Crear y modificar avances de SU proyecto. |
| **Ingeniero** | Creación de Subcontratos, validación de Avances. | Acceso completo a Subcontratos y Avances de su proyecto. |
| **Contadora** | Gestión y procesamiento de pagos. | Acceso a facturas generadas y reportes contables. |
| **Gerente** | Supervisión y Liberación de Garantías. | Acceso total y permisos para usar el asistente de liberación. |

## ⚙️ Dependencias

Este módulo requiere las siguientes dependencias técnicas para su correcto funcionamiento:

* `base`
* `mail` (Para el Chatter y notificaciones)
* `account` (Gestión contable y facturación)
* `project` (Vinculación con proyectos existentes)
* `purchase` (Órdenes de compra base, opcional)
* `l10n_do` (Localización Dominicana, si aplica)

---
**Desarrollado por:** Construcciones Lamout S.R.L.
**Website:** https://www.construccioneslamout.com


 =========================================================================
# DOCUMENTACIÓN: GUÍA DE ASIGNACIÓN DE ROLES
# =========================================================================

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                     GUÍA DE ROLES Y PERMISOS                               ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROL 1: CAPATAZ / MAESTRO DE OBRA                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Usuario Típico: Juan (Capataz Torre), Pedro (Capataz Proyecto Rony)        │
│                                                                             │
│ ✅ PUEDE:                                                                   │
│   • Ver subcontratos de SU proyecto asignado                               │
│   • Crear avances de obra (registrar cantidad ejecutada)                   │
│   • Subir fotos como evidencia                                             │
│   • Enviar avances para validación del ingeniero                           │
│   • Ver estado de sus avances (draft, pending, validated)                  │
│                                                                             │
│ ❌ NO PUEDE:                                                                │
│   • Ver proyectos de otros capataces                                       │
│   • Validar sus propios avances                                            │
│   • Modificar contratos o precios                                          │
│   • Eliminar registros                                                     │
│   • Liberar garantías                                                      │
│                                                                             │
│ 📱 ACCESO: Tablet en obra con conexión WiFi/4G                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROL 2: INGENIERO RESIDENTE                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Usuario Típico: Ing. Carlos (Residente), Ing. María (Supervisora)          │
│                                                                             │
│ ✅ PUEDE:                                                                   │
│   • Ver TODOS los proyectos y subcontratos                                 │
│   • Crear y modificar contratos (draft)                                    │
│   • Validar avances de obra                                                │
│   • Rechazar avances con justificación                                     │
│   • Ver reportes de productividad                                          │
│   • Modificar tareas y cronograma                                          │
│                                                                             │
│ ❌ NO PUEDE:                                                                │
│   • Eliminar contratos activos o completados                               │
│   • Liberar garantías (solo Gerente)                                       │
│   • Modificar % de retención de garantía                                   │
│   • Eliminar avances validados                                             │
│                                                                             │
│ 💻 ACCESO: PC de oficina + Tablet para visitas a obra                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROL 3: GERENTE DE CONSTRUCCIÓN                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Usuario Típico: Tú (Dueño/Gerente General)                                 │
│                                                                             │
│ ✅ PUEDE (ACCESO TOTAL):                                                    │
│   • TODO lo que puede el Ingeniero +                                       │
│   • Eliminar cualquier registro (con auditoría)                            │
│   • Liberar garantías retenidas                                            │
│   • Modificar % de retención de garantía                                   │
│   • Ver Dashboard ejecutivo completo                                       │
│   • Aprobar pagos finales                                                  │
│   • Acceso a reportes financieros sensibles                                │
│                                                                             │
│ 🎯 RESPONSABILIDADES:                                                       │
│   • Supervisión financiera general                                         │
│   • Aprobación de contratos > $100k (configurable)                         │
│   • Liberación de fondos de garantía al finalizar obras                    │
│                                                                             │
│ 💻 ACCESO: PC oficina + Mobile app                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROL 4: CONTADORA (Permisos especiales)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Usuario Típico: Marta (Contadora)                                          │
│                                                                             │
│ ✅ PUEDE:                                                                   │
│   • Ver todos los subcontratos y avances (solo lectura)                    │
│   • Modificar campos contables (cuentas, centros de costo)                 │
│   • Generar y aprobar facturas de proveedor                                │
│   • Ejecutar pagos desde módulo de contabilidad                            │
│   • Descargar reportes 606/607                                             │
│   • Ver garantías retenidas pendientes                                     │
│                                                                             │
│ ❌ NO PUEDE:                                                                │
│   • Validar avances técnicos de obra                                       │
│   • Modificar cantidades ejecutadas                                        │
│   • Cambiar precios unitarios                                              │
│                                                                             │
│ 💻 ACCESO: PC oficina, módulo Contabilidad principalmente                   │
└─────────────────────────────────────────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════╗
║                    FLUJO DE TRABAJO CON ROLES                              ║
╚════════════════════════════════════════════════════════════════════════════╝

LUNES - SÁBADO (Ejecución):
   1. 👷 Capataz: Registra avance diario/semanal desde tablet
      → Crea registro en estado "draft"
      → Sube fotos de la obra

SÁBADO (Cierre Semanal):
   2. 👷 Capataz: Envía avance para validación
      → Cambia a estado "pending"
      → Notificación automática al Ingeniero

   3. 👨‍💼 Ingeniero: Revisa evidencias y valida
      → Si OK: Cambia a "validated" → genera factura
      → Si NO: Rechaza con motivo → regresa a capataz

   4. 👩‍💼 Contadora: Registra pago
      → Ve factura generada automáticamente
      → Aplica retención 20% (garantía)
      → Ejecuta pago del 80% restante

FIN DE OBRA:
   5. 👨‍💼 Ingeniero: Marca contrato como "completed"
   
   6. 🎩 Gerente: Libera garantía retenida
      → Revisa que obra está perfecta (sin defectos)
      → Libera el 20% final → genera pago

╔════════════════════════════════════════════════════════════════════════════╗
║                    SEGURIDAD Y AUDITORÍA                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ LOGS AUTOMÁTICOS (Chatter):
   • Quién creó el registro y cuándo
   • Quién validó el avance (con fecha/hora)
   • Quién modificó montos (histórico completo)
   • Quién liberó la garantía

✅ RESTRICCIONES TÉCNICAS:
   • No se puede validar avances sin foto adjunta (personalizable)
   • No se puede pagar más del 110% del contrato estimado
   • No se puede eliminar avances validados (solo Gerente con motivo)
   • Cambios en montos >10% requieren aprobación adicional

✅ BACKUP Y TRAZABILIDAD:
   • Todos los cambios en campos financieros se registran
   • Backup automático diario (configurar en AWS/Odoo.sh)
   • Exportación de auditoría disponible para DGII

"""

# =========================================================================
# SCRIPT DE INSTALACIÓN Y ASIGNACIÓN DE ROLES
# Para ejecutar después de instalar el módulo
# =========================================================================

"""
# Ejecutar en shell de Odoo (odoo-bin shell -d tu_base_de_datos)

from odoo import api, SUPERUSER_ID

def setup_users_and_roles():
    '''
    Script para crear usuarios de ejemplo y asignar roles
    IMPORTANTE: Ejecutar solo en desarrollo, en producción crear usuarios manualmente
    '''
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Referencias a grupos
        group_foreman = env.ref('construction_subcontracts.group_construction_foreman')
        group_engineer = env.ref('construction_subcontracts.group_construction_engineer')
        group_manager = env.ref('construction_subcontracts.group_construction_manager')
        
        # 1. CREAR USUARIO CAPATAZ (Ejemplo)
        capataz = env['res.users'].create({
            'name': 'Juan Pérez (Capataz Torre)',
            'login': 'juan.capataz',
            'email': 'juan@construccioneslamout.com',
            'groups_id': [(6, 0, [group_foreman.id])],
        })
        print(f"✅ Usuario Capataz creado: {capataz.login}")
        
        # 2. CREAR USUARIO INGENIERO
        ingeniero = env['res.users'].create({
            'name': 'Ing. Carlos Rodríguez',
            'login': 'carlos.ingeniero',
            'email': 'carlos@construccioneslamout.com',
            'groups_id': [(6, 0, [group_engineer.id])],
        })
        print(f"✅ Usuario Ingeniero creado: {ingeniero.login}")
        
        # 3. ASIGNAR TU USUARIO COMO GERENTE
        # Busca tu usuario actual
        tu_usuario = env['res.users'].search([('login', '=', 'admin')], limit=1)
        if tu_usuario:
            tu_usuario.write({
                'groups_id': [(4, group_manager.id)]
            })
            print(f"✅ Usuario {tu_usuario.name} asignado como Gerente")
        
        # 4. DAR ACCESO DE LECTURA A CONTADORA
        contadora = env['res.users'].search([('login', '=', 'marta')], limit=1)
        if contadora:
            # La contadora ya tiene grupo de facturación, solo agregamos lectura
            print(f"✅ Contadora {contadora.name} tiene acceso de lectura automático")
        
        env.cr.commit()
        print("\\n🎉 Configuración de usuarios completada!")

# Ejecutar función
setup_users_and_roles()
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVOS DE SEGURIDAD GENERADOS                           ║
╚════════════════════════════════════════════════════════════════════════════╝

📁 security/
  ├── security.xml          → Grupos de usuarios y reglas de registro
  ├── ir.model.access.csv   → Permisos CRUD por modelo
  └── README.md             → Esta documentación

📁 data/
  └── sequences.xml         → Numeración automática (SC-0001, AV-2025-0001)

✅ PRÓXIMOS PASOS:
1. Copiar estos archivos a tu módulo Odoo
2. Actualizar el módulo: odoo-bin -u construction_subcontracts
3. Ir a Configuración > Usuarios y Compañías > Usuarios
4. Asignar grupos a cada usuario según su rol