# -*- coding: utf-8 -*-
{
    'name': 'Real Estate',
    'version': '1.7',
    'summary': 'Real Estate Management',
    'sequence': 10,
    'description': """
Real Estate Management
======================
The Real Estate Management module in Odoo allows you to manage your real estate properties, tenants, and rental agreements. It provides an easy way to follow up on your tenants and properties.""" ,
    'category': 'Real Estate/Real Estate',
    'website': '',
    'depends': ['base'],
    'data': ['security/ir.model.access.csv',
             'views/estate_property_views.xml',
             'views/estate_menus.xml',
             'views/estate_property_searchs.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_tag_views.xml',
             'views/estate_property_offer_views.xml',
             'views/res_users_views_inherit.xml',
            ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}