# -*- coding: utf-8 -*-
{
    'name': "Delivry Custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    "author": "Azkatech",

    'website': "https://azka.tech",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['stock','sale'],

    'data': [
        'views/views.xml',
        'views/delivrey_report.xml',
    ],

}
