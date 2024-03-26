from odoo import models, api, fields, _
from datetime import timedelta
from odoo.exceptions import UserError


STATUS = [
    ('refused', 'Refused'),
    ('accepted', 'Accepted'),
]

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'Price must be positive.'),
    ]

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
    
    validity = fields.Integer(string='Validity')
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_deadline',
        inverse='_inverse_validity',
        readonly=False,
    )

    property_type_id = fields.Many2one(
        string='Property Type',
        related='property_id.property_type',
    )
    
    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)
                
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accept(self):
        self.ensure_one()
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id.id
        self.property_id._onchange_offer_ids()
        return True 
    
    def action_offer_refuse(self):
        self.ensure_one()
        self.status = 'refused'
        self.property_id._onchange_offer_ids()
        return True

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])

        if vals['price'] < property_id.selling_price:
            raise UserError(_('Offer price should not be less than current selling price'))
        property_id.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)