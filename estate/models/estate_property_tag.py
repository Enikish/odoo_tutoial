from odoo import models, fields, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name field must be unique.'),
    ]

    name = fields.Char(
        string='Name',
        required=True,
        )
    
    
    