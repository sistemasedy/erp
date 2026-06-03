# -*- coding: utf-8 -*-
################################################################################
#
#    Kolpolok Ltd. (https://www.kolpolok.com)
#    Author: Kaushik Ahmed Apu, Aqil Mahmud, Zarin Tasnim(<https://www.kolpolok.com>)
#
################################################################################


{
    'name': "Hide Menu | Show or Hide Password",
    'summary': """
         This module enhances security and user experience by restricting menu access based on roles and toggling password visibility during login""",
    'description': """
       """,
    'author': 'Kolpolok',
    'maintainer':'kolpolok',
    'website': "https://www.kolpolok.com",
    'images': ["static/description/banner.gif"],
    'category': 'Extra Tools/Website',
    'version': "15.0.1.0.0",
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'views/res_users.xml',
        'views/login_page.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'kolpolok_hide_menu/static/src/scss/style.scss',
            'kolpolok_hide_menu/static/src/js/custom.js',
        ],
    },
}
