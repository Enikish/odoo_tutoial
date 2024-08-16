{
    'name': 'My library',
    'author': 'Enish', 
    'version': '17.0.0.1',
    'application': 'true',
    'installable': 'true',
    'depends': ['base', 'product'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book_category.xml',
        'views/library_book.xml',
        'views/library_member.xml',
        'views/library_book_rent.xml',
             ],
    'license': 'LGPL-3',
    'demo':[
        'data/data.xml',
    ]

}