from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name field must be unique.'),
    ]

    name = fields.Char(
        string='Name',
        required=True,
        )
    
    property_ids = fields.One2many(
        string='Properties',
        comodel_name='estate.property',
        inverse_name='property_type',
    )

    sequence = fields.Integer(
        string='Sequence',
        default=1,
    )

    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
    )

    offer_count = fields.Integer(
        string='Offer count',
        compute='_compute_offer_count',
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


    