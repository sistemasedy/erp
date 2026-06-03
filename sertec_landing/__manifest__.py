# -*- coding: utf-8 -*-
{
    'name': 'Landing Page Edy Mejía',
    'version': '15.0.1.0.0',
    'summary': 'Sirve la landing page y captura leads en el CRM desde CloudClusters',
    'author': 'Edy Mejía',
    'website': 'https://edymejia.com',
    'license': 'LGPL-3',

    'depends': ['base', 'crm', 'website'],

    'data': [
        'data/crm_stage_data.xml',
        'views/landing_template.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
