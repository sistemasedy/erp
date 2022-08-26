# -*- coding: utf-8 -*-
{
    'name': "web_sitets",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    #'depends': ['base','website','web','web_editor','website_sale'],
    'depends': ['base','point_of_sale','website','web','website_sale','stock_account', 'barcodes', 'web_editor', 'digest'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/customer/customer.xml',
        'views/index.xml',
        'views/templates.xml',
        'views/template_tes.xml',
        'views/template_js.xml',
        'views/aset.xml',
        #'views/app/assets.xml',
        'views/app/app.xml',
        'views/app/todo_app.xml',
        'views/app_inventory/inventory/inventory.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
        'static/src/xml/tes.xml',
        'static/src/xml/debug_manager.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}