# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
#################################################################################
{
    'name': 'EM POS Keyboard Search',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'This Payment | POS Custom Receipt',
    'website': 'www.kanakinfosystems.com',
    'author': 'Kanak Infosystems LLP.',
    'images': ['static/description/banner.jpg'],
    'description': "Customized our point of sale receipt",
    'depends': ['base', 'point_of_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'demo': [],
    "qweb": [
        #"static/src/xml/pos_margin.xml",
        'static/src/xml/Screens/ProductScreen/product_create_button.xml',
        'static/src/xml/Screens/ProductScreen/product_create_popup.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidgetControlPanel.xml',
        'static/src/xml/Screens/ProductScreen/ProductItem.xml',
        'static/src/xml/Screens/ProductScreen/ProductList.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidget.xml',
    ],
    'installable': True,
}
