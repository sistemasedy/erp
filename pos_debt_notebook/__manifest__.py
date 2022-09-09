# Copyright 2014-2019 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2015 Bassirou Ndaw <https://github.com/bassn>
# Copyright 2015 Alexis de Lattre <https://github.com/alexis-via>
# Copyright 2016-2017 Stanislav Krotov <https://it-projects.info/team/ufaks>
# Copyright 2017 Ilmir Karamov <https://it-projects.info/team/ilmir-k>
# Copyright 2017 Artyom Losev
# Copyright 2017 Lilia Salihova
# Copyright 2017-2018 Gabbasov Dinar <https://it-projects.info/team/GabbasovDinar>
# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": "EM POS: Prepaid credits",
    "summary": "Comfortable sales for your regular customers. Debt payment method for POS",
    "category": "Point Of Sale",
    "images": ["images/debt_notebook.png"],
    "version": "14.0.5.3.4",
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://github.com/itpp-labs/pos-addons/",
    "license": "Other OSI approved licence",  # MIT
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["point_of_sale"],
    "data": [
        "security/pos_debt_notebook_security.xml",
        "data/product.xml",
        "views/pos_debt_report_view.xml",
        "views.xml",
        "views/pos_credit_update.xml",
        "wizard/pos_credit_invoices_views.xml",
        "wizard/pos_credit_company_invoices_views.xml",
        "security/ir.model.access.csv",
    ],
    'assets': {
        'point_of_sale.assets': [
                'pos_debt_notebook/static/src/css/pos.css',
                'pos_debt_notebook/static/src/js/pos.js',
                'pos_debt_notebook/static/src/js/CreditNote.js',
                'pos_debt_notebook/static/src/js/OrderReceipt.js',
                'pos_debt_notebook/static/src/js/ReceiptScreen.js',
                'pos_debt_notebook/static/src/js/ValidationButton.js',
                'pos_debt_notebook/static/src/js/DebtHistoryLine.js',
        ],
        'web.assets_backend': [
                'pos_debt_notebook/static/src/js/test_pos_debt.js',
        ],
        'web.assets_qweb': [
            'pos_debt_notebook/static/src/xml/CreditNote.xml',
            'pos_debt_notebook/static/src/xml/OrderReceipt.xml',
            'pos_debt_notebook/static/src/xml/PaymentMethodButton.xml',
            'pos_debt_notebook/static/src/xml/ReceiptScreen.xml',
            'pos_debt_notebook/static/src/xml/pos.xml',
        ],
    },
    "demo": ["data/demo.xml"],
    "installable": True,
    "uninstall_hook": "pre_uninstall",
}
