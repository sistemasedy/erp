# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'POS Base kanak',
    'summary': 'This odoo module is the base module of various pos reports - pos_item_sale_report, pos_hourly_sales_report, pos_table_sales_report, pos_item_inventory_report, pos_receipt_information, and pos_void_report.',
    'category': 'Point of Sale',
    'description': """
POS Base Module
====================================================================================
    """,
    'version': '15.0.1.0',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'depends': [
        'point_of_sale',
        'pos_restaurant',
        'stock_account'
    ],
    'data': [
        'reports/report_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True
}
