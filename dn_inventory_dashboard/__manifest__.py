# -*- coding: utf-8 -*-
{
    'name': "Inventory Dashboard",
    'summary': "Inventory Dashboard Information",
    'description': """
        Inventory Dashboard Information
    """,
    'author': "Dimas Nugraha",
    'website': "",
    'category': 'Inventory',
    'version': '1',
    'depends': ['stock', 'web'],
    'data': [
        'views/views.xml',
        'views/assets_load.xml',
    ],
    'qweb': ['static/src/xml/inventory_dashboard_templates.xml'],
    'installable': True,
}
