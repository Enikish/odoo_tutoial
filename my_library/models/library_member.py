from odoo import fields, api, models, _

class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    
    date_start = fields.Date(string='Member Since')
    date_end = fields.Date(string='Membership End Date')
    member_number = fields.Char(string='Member Number')
    date_of_birth = fields.Date(string='Date of Birth')