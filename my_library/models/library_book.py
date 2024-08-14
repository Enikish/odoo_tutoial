from odoo import fields, models, _, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


_STATE = [
    ('draft', 'Not Available'),
    ('available', 'Available'),
    ('borrowed', 'Borrowed'),
    ('lost', 'Lost'),
]

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'name'

    _inherit = ['base.archive']

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)', 'Number of pages must be positive.')
    ]

    def name_get(self):
        result = []
        for book in self:
            authors = book.author_ids.mapped('name')
            name = '%s(%s)' % (book.name, ','.join(authors))
            result.append((book.id, name))
            return result
        
    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', 
                     limit=100, order=None):
        domain = [] if domain is None else domain.copy()
        if not ( name == '' and operator == 'ilike'):
            domain += ['|', 
                        '|',
                        ('name', operator, name),
                        ('isbn', operator, name),
                     ('author_ids.name', operator, name)
                     ]
            
            return super(LibraryBook, self)._name_search(
                name=name, domain=domain, operator=operator, 
                limit=limit, order=order
            )
    old_edition = fields.Many2one(comodel_name='library.book', string='Old Edition')

    
    name = fields.Char(string='Title', required=True)
    short_name = fields.Char(string='Short Title', required=True)
    description = fields.Html(string='Description')
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print?')
    date_release = fields.Date(string='Release Date', default=lambda self: fields.Date.today())
    date_updated = fields.Datetime(string='Last Updated')
    pages = fields.Integer(string='Number of Pages')
    isbn = fields.Char('ISBN')
    reader_rating = fields.Float(string='Reader Rating', digits=(14, 4))
    author_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Authors',
    )

    note = fields.Text(string='Internal Notes')
    state = fields.Selection(
        string='State',
        selection=_STATE,
        default='available',
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
    
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed
    
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed' % (book.state, new_state))
                raise UserError(msg)
    
    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        all_members = library_member_model.search([])
        print('All members', all_members)
        return True

    def change_release_date(self):
        self.ensure_one()
        self.date_release = fields.Date.today()

    def find_book(self):
        domain = [
            '|',
            '&',('name', 'ilike', '300'),
            ('category_id.name', 'ilike', 'Fic'),
            '&',('name', 'ilike', 'Book Name 2'),
            ('category_id.name', 'ilike', 'Category Name 2')
        ]

        books = self.search(domain=domain)

        print(books)

    @api.model
    def books_with_multiple_authors(self, all_books):
        def predicate(book):
            if len(book.author_ids) > 1:
                return True
            return False
        return all_books.filter(predicate)
    
    @api.model
    def get_author_names(self, books: models.Model):
        return books.mapped('author_ids.name')
    
    @api.model
    def sort_books_by_date(self, books: models.Model):
        return books.sorted(key='release_date', reverse=True)
    
    manager_remarks = fields.Text(string='Manager Remarks')

    @api.model
    def create(self, values):
        if not self.user_has_groups('my_library.group_librarian'):
            if 'manager_remarks' in values:
                raise UserError(_('You are not allowed to modify \'manager_remarks\' '))
        return super(LibraryBook, self).create(values)
    
    def write(self, vals):
        if not self.user_has_groups('my_library.group_librarian'):
            if 'manager_remarks' in vals:
                raise UserError(_('You are not allowed to modify \'manager_remarks\' '))
        return super().write(vals)
    
    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [('cost_price', '!=', False),], # domain
            ['category_id', 'cost_price:avg'], # field to access
            ['category_id'] # group_by
            )
        return grouped_result
    
    def log_avg_cost(self):
        print(self._get_average_cost())

    