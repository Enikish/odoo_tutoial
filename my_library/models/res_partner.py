from odoo import fields, models, _, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book = fields.One2many(comodel_name='library.book',
                                     inverse_name='publisher_id',
                                     string='Published Book')

    authored_book_ids = fields.Many2many(comodel_name='library.book',
                                         string='Authored Books')