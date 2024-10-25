from odoo import fields, models


class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = 'Information about hotel'
    name = fields.Char(string='Hostel Name', required=True)
    hostel_code = fields.Char(string='Code', required=True)
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    state_id = fields.Many2one('res.country.state', string='State')
    
