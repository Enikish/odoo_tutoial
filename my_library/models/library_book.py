from odoo import fields, models, _

class LibraryBook(models.Model):
    _name = 'library.book'
    
    name = fields.Char(string='Title', required=True)
    date_release = fields.Date(string='Release Date')
    author_ids = fields.Many2many(
        comodel_name='res.parner',
        string='Authors',
    )
    