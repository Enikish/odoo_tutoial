from odoo import fields, models, _, api
from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import timedelta


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

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id,
    )

    cost_price = fields.Monetary(
        string='Book Cost',
        currency_field='currency_id',
        digits=(16, 2),
    )

    retail_price = fields.Monetary(
        string='Retail Price',
        currency_field='currency_id',
        digits=(16, 2),
    )

    publisher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Publisher',
        ondelete='set null',
        context={},
        domain=[],
    )

    publisher_city = fields.Char(
        string='Publisher City',
        related='publisher_id.city',
        readonly=True
    )

    category_id = fields.Many2one(
        comodel_name='library.book.category',
        string='Category',
    )

    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        help="Number of days since the book was released.",
    )

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release > fields.Date.today():
                raise ValidationError(_('Release date must be in the past.'))
            
    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('age_days'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<',
            '>=': '<=',
            '<': '>',
            '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    ref_doc_id = fields.Reference(
        string='Reference Document',
        selection='_referencable_models',
    )
    
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name','=','message_ids')])
        return [(model.model, model.name) for model in models]
    