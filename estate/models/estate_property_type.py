from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(
        string='name',
        required=True,
        )