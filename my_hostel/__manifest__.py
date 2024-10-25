{
    'name': 'Hostel Management',
    'summary': 'Manage Hostel easily',
    'description': 'Effeciently manage the entire reidential facility in the school.',
    'author': 'Enish',
    'category': 'Hostel',
    'version': '17.0.1.0.0',
    'data': [
        'security/hostel_security.xml',
        'security/ir.model.access.csv',
        'views/hostel.xml',
    ],
    'depends': ['base'],
        'assets': {
            'web.assets_backend': [
            'web/static/src/xml/**/*',
        ],
    },
    'applicatioin': True,
    'installable': True,
    'license': 'LGPL-3',
    # 'demo': ['demo.xml'],
}