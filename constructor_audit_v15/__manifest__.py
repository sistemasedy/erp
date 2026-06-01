{
    'name': 'Constructor Audit – Inspección de Resistencia Operativa',
    'version': '15.0.1.0.0',
    'category': 'Construction/Productivity',
    'summary': 'Diagnóstico automatizado de eficiencia para constructoras',
    'author': 'Constructor Audit',
    'license': 'LGPL-3',
    'depends': [
        'survey',
        'crm',
        'mail',
        'website',
        'base_automation',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_tags.xml',
        'data/survey_data.xml',
        'views/crm_lead_views.xml',
        'views/audit_config_views.xml',
        'data/email_templates.xml',
        'data/automated_actions.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'constructor_audit_v15/static/src/css/audit_styles.css',
            'constructor_audit_v15/static/src/js/roi_calculator.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
}
