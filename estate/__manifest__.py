{
    'name': 'Real Estate',
    'version': '14.0.1',
    'category': 'sales, real estate',
    'summary': 'This is an essay module of a real estate business model',
    'description': """
        In this module, a practice of the entire documentation course that is found within the main page of Odoo is carried out, 
        it is a module of a real estate company and therefore it has all the basic functionalities of a business model of this type.
    """,
    'author': 'Isaac Blanco',
    'website': 'None',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        #'views/inherited_model_users_views.xml'
    ],
    'demo': [
        #'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
