from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

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