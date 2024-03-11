from odoo import models, api, fields
from datetime import timedelta


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
    
    validity = fields.Integer(string='Validity')
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_deadline',
        inverse='_inverse_validity',
        readonly=False,
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
        return True
    
    def action_offer_refuse(self):
        self.ensure_one()
        self.status = 'refused'
        return True
