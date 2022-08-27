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
    'assets': {
        'point_of_sale.assets': [
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/ProductScreens.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/product_create_popup.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/product_create_button.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/ListProducts.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/ProductItem.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/ProductItemSearch.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/ProductListSearch.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/ProductsWidgetControlPanelSearch.js',
            '/em_keyboard_search_pos/static/src/js/Screens/ProductScreen/ProductsWidgetSearch.js',
            '<link rel="stylesheet" href="/em_keyboard_search_pos/static/src/css/pos.css">',
        ],
        'web.assets_qweb': [
            '/em_keyboard_search_pos/static/src/xml/Screens/ProductScreen/product_create_button.xml',
            '/em_keyboard_search_pos/static/src/xml/Screens/ProductScreen/product_create_popup.xml',
            '/em_keyboard_search_pos/static/src/xml/Screens/ProductScreen/ProductsWidgetControlPanel.xml',
            '/em_keyboard_search_pos/static/src/xml/Screens/ProductScreen/ProductItem.xml',
            '/em_keyboard_search_pos/static/src/xml/Screens/ProductScreen/ProductList.xml',
            '/em_keyboard_search_pos/static/src/xml/Screens/ProductScreen/ProductsWidget.xml',

        ],
    },
    'demo': [],
    'installable': True,
}
