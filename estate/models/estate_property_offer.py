from odoo import models, api, fields

STATUS = [
    ('refused', 'Refused'),
    ('accepted', 'Accepted'),
]

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Integer(string='Price')
    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        required=True,
    )
    status = fields.Selection(
        string='Status',
        selection=STATUS,
        copy=False,
    )
    property_id = fields.Many2one(
        string='Estate Property',
        comodel_name='estate.property',
        required=True,
    )
    