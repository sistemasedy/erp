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
    'name': 'EM pos Receipt',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'This Payment | POS Custom Receipt',
    'website': 'www.kanakinfosystems.com',
    'author': 'Kanak Infosystems LLP.',
    'images': ['static/description/banner.jpg'],
    'description': "Customized our point of sale receipt",
    'depends': ['base', 'point_of_sale'],
    "data": [],
    'demo': [],
    "qweb": [
        "static/src/xml/pos.xml",
        'static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
    ],
    'installable': True,
}
