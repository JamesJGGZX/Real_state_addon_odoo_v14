# -*- coding: utf-8 -*-
{
    'name': "Modulo Ensayo",
    'summary':"""
        Ensayo de un modulo en Odoo 14, con sus funcionalidades básicas
    """,
    'author':'Isaac Blanco',
    'category':'General',
    'version':'14.0.1',
    'depends':['mail','hr'],
    'data':[
        'views/menu_view.xml',
        'views/libros_view.xml',
        'security/libreria_security.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
    ],
}