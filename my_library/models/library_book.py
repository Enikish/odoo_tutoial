from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


_STATE = [
    ('draft', 'Not Available'),
    ('available', 'Available'),
    ('lost', 'Lost'),
]

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'name'

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)', 'Number of pages must be positive.')
    ]
    
    name = fields.Char(string='Title', required=True)
    short_name = fields.Char(string='Short Title', required=True)
    description = fields.Html(string='Description')
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print?')
    date_release = fields.Date(string='Release Date')
    date_updated = fields.Datetime(string='Last Updated')
    pages = fields.Integer(string='Number of Pages')
    reader_rating = fields.Float(string='Reader Rating', digits=(14, 4))
    author_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Authors',
    )

    note = fields.Text(string='Internal Notes')
    state = fields.Selection(
        string='State',
        selection=_STATE,
    )

    curreny_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
    )

    cost_price = fields.Monetary(
        string='Book Cost',
        currency_field='curreny_id',
        digits=(16, 2),
    )

    retail_price = fields.Monetary(
        string='Retail Price',
        currency_field='curreny_id',
        digits=(16, 2),
    )

    publisher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Publisher',
        ondelete='set null',
        context={},
        domain=[],
    )

    category_id = fields.Many2one(
        comodel_name='library.book.category',
        string='Category',
    )

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release > fields.Date.today():
                raise ValidationError(_('Release date must be in the past.'))