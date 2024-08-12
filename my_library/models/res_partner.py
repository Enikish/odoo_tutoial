from odoo import fields, models, _, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book = fields.One2many(comodel_name='library.book',
                                     inverse_name='publisher_id',
                                     string='Published Book')

    authored_book_ids = fields.Many2many(comodel_name='library.book',
                                         string='Authored Books')
    
    count_books = fields.Integer(string='Number of Books',
                                 compute='_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for record in self:
            record.count_books = len(record.authored_book_ids)
    