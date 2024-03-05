{
    'name': 'estate',
    'application': True,
    'version': '17.0.0.1',
    'summary': 'Odoo官方教程练习',
    'dependencies': ['base'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'data/estate_property_type_demo.xml',
        'data/estate_property_tag_demo.xml',
    ]
}