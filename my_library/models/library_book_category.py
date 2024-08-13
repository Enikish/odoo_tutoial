from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class BookCategory(models.Model):
    _name = 'library.book.category'
    name = fields.Char(string='Category')
    parent_id = fields.Many2one(
        comodel_name='library.book.category',
        string='Parent Category',
        ondelete='restrict',
        index=True,
    )

    description = fields.Text(string='Description')

    child_ids = fields.One2many(
        comodel_name='library.book.category',
        inverse_name='parent_id',
        string='Child Categories',
    )

    _parent_store = True
    _parent_name = 'parent_id'
    parent_path = fields.Char(index=True)


    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }

        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }

        parent_category_val = {
            'name': 'Parent category',
            'description': 'Desciption for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }

        record = self.env['library.book.category'].create(parent_category_val)

        