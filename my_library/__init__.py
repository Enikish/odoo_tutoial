from odoo import api, fields, SUPERUSER_ID

from . import models
from . import controllers
from . import wizard

def add_book_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    book_data1 = {'name': 'Piece and war', 'date_release': fields.Date.today(), 'short_name': 'Piece&War'}
    book_data2 = {'name': 'HarryPotter', 'date_release': fields.Date.from_string('1997-06-30'), 'short_name': 'Wizards'}
    env['library.book'].create([book_data1, book_data2])
