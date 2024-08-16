from odoo import models, fields, api, _


_STATE = [
    ('ongoing', 'Ongoing'),
    ('returned', 'Returned'),
    ('lost', 'Lost')
]

class LibraryBookRent(models.Model):
    _name = 'library.book.rent'
    _description = 'Library Rent'
    _rec_name = 'book_id'
    
    def name_get(self):
        result = []
        for rent in self:
            book = rent.book_id.name
            borrower = rent.borrower_id.name
            result.append((rent.id,(book,borrower)))
        return result

    book_id = fields.Many2one(comodel_name='library.book',
                              string='Book',
                              required=True)
    
    borrower_id = fields.Many2one(comodel_name='res.partner',
                                  string='Borrower',
                                  required=True)
    
    state = fields.Selection(selection=_STATE,
                             default='ongoing',
                             required=True)
    
    rent_date = fields.Date(string='Rent Date',
                            default=fields.Date.today)

    return_date = fields.Date(string='Return Date')

    def book_lost(self):
        self.ensure_one()
        self.sudo().state = 'lost'
        book_with_different_context = self.book_id.with_context(avoid_deactive=True)
        book_with_different_context.sudo().make_lost()
        
