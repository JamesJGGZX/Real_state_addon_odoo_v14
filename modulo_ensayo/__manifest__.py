# -*- coding: utf-8 -*-
{
    'name': "Modulo Ensayo",
    'summary':"""
        Ensayo de un modulo en Odoo 14, con sus funcionalidades básicas
    """,
    'author':'Isaac Blanco',
    'category':'General',
    'version':'1.0.0',
    'depends':['mail'],
    'data':[
        'views/menu_view.xml',
        'views/libros_view.xml',
        'security/libreria_security.xml',
        'security/ir.model.access.csv',
    ],
}