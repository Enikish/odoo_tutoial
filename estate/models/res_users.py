from odoo import fields, api, _, models


class ResUsers(models.Model):
    _inherit = 'res.users'    
    property_ids = fields.One2many(
        string='Property Id',
        comodel_name='estate.property',
        inverse_name='salesman',
        domain=[('active', '=', True)],
    )
    