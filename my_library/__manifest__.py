{
    'name': 'My library',
    'author': 'Enish', 
    'version': '17.0.0.1',
    'application': 'true',
    'installable': 'true',
    'depends': ['base', 'product', 'account', 'project'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book_category.xml',
        'views/library_book.xml',
        'views/library_member.xml',
        'views/library_book_rent.xml',
        'wizard/library_rent_wizard.xml',
        'wizard/library_return_wizard.xml',
        'views/library_book_rent_statistics.xml',
        'views/res_config_settings.xml',
        'views/res_partner.xml',
        'views/project_task.xml',
             ],
    'license': 'LGPL-3',
    'demo':[
        'data/data.xml',
    ],
    'post_init_hook': 'add_book_hook',

}