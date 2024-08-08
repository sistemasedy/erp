# -*- coding: utf-8 -*-
{
    'name': "EM PRODUCTO",

    'summary': """
        PERSONALIZACION DEL MODULO PRODUCTOS""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','base_setup', 'product','sale','point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/template.xml',
        'report/report.xml',
        'report/report_list.xml',
        'views/invoice/report.xml',
        'views/sale/order.xml',
        'views/sale/order_views.xml',
        'views/invoice/invoice_template.xml',
        'views/invoice/punto_venta.xml',
        'report/inventory/list_code.xml',
        #'views/layouts.xml',
        #'views/assets.xml',
        #'views/about.xml',
        #'views/pages_top.xml',
        #'views/contact_us.xml',
        #'views/footer.xml',
        #'views/header.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        #'static/src/xml/pos.xml',
    ],
}