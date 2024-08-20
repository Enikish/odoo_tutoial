from odoo import fields, models, api, _
from odoo.exceptions import UserError


class LibraryRentWizard(models.TransientModel):
    _name = 'library.rent.wizard'

    borrower_id = fields.Many2one(comodel_name='res.partner',
                                  string='Borrower',
                                  default=lambda self: self.env.user.partner_id.id)
    book_ids = fields.Many2many(comodel_name='library.book', 
                                string='Books')
    
    expected_return_date = fields.Date(string='Expected Return Date')

    def add_book_rents(self):
        rentModel = self.env['library.book.rent']
        for wiz in self:
            for book in wiz.book_ids:
                rentModel.create({'borrower_id': wiz.borrower_id.id,
                                  'book_id': book.id,
                                  'expected_return_date': wiz.expected_return_date or None})
        borrowers = self.mapped('borrower_id')
        action = borrowers.get_formview_action()
        if len(borrowers.ids) > 1:
            action['domain'] = [('id', 'in', tuple(borrowers.ids))]
            action['view_mode'] = 'tree,form'
        return action


    