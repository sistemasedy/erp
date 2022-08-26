# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "PoS Order Margin",
    "summary": "Margin on PoS Order",
    "version": "14.0.1.0.1",
    "category": "Point Of Sale",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/pos",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale","account",
    ],
    "data": [
        "views/templates.xml",
    ],
    "qweb": [
        "static/src/xml/pos_margin.xml",
        "static/src/xml/pos_clear_cart.xml",
        'static/src/xml/Screens/ProductScreen/product_create_button.xml',
        'static/src/xml/Screens/ProductScreen/product_create_popup.xml',
        'static/src/xml/Screens/ProductScreen/PaymentDirect.xml',
        'static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidgetControlPanel.xml',
        'static/src/xml/Screens/ProductScreen/ProductItem.xml',
        'static/src/xml/Screens/ProductScreen/ProductList.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidget.xml',
    ],
    "installable": True,
}
