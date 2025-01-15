{
    'name': 'List Due Invoices',
    'version': '15.0.1.1',
    'summary': 'List Due Invoices',
    'description': """
List Due Invoices
=================

This module lists (customer or vendor) invoices on or before the due date selected.


Keywords: Odoo Due Customer Invoices, Odoo Due Vendor Invoices, Odoo Due Supplier Invoices,
Odoo Due Vendor Bills, Odoo Due Invoices
""",
    'category': 'Accounting/Accounting',
    'author': 'MAC5',
    'contributors': ['MAC5'],
    'website': 'https://apps.odoo.com/apps/modules/browse?author=MAC5',
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        #'wizard/account_invoice_due_list_view.xml',
        'wizard/customer_deposit_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
    'support': 'mac5_odoo@outlook.com',
    'license': 'LGPL-3',
    'live_test_url': 'https://youtu.be/QXcP9yvsRiI',
}
