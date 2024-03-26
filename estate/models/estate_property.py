from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

GARDEN_ORIENTATION = [
    ('north', 'North'),
    ('south', 'South'),
    ('east', 'East'),
    ('west', 'West'),
]

STATE = [
    ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled'),
]

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char(
        string='Name', 
        required=True, 
        default='Unknown',
    )
    description = fields.Text(string='Description')
    postcode = fields.Char(string='PostCode')
    date_availability = fields.Date(
        string='Date Availability',
        default=fields.Date.add(fields.Date.today(), days=30),  # 时间从今天计算往后推30天，可以使用-30变成提前30天
    )
    expected_price = fields.Float(
        string='Expected Price', 
        required=True,
    )
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=GARDEN_ORIENTATION,
    )
    last_seen = fields.Datetime(
        string='Last Seen',
        default=fields.Datetime.now,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    state = fields.Selection(
        string='State',
        selection=STATE,
        default='new',
        readonly=False,
    )
    salesman = fields.Many2one(
        string='Salesman',
        comodel_name='res.users',
        default=lambda self: self.env.user,
    )
    buyer = fields.Many2one(
        string='Buyer',
        comodel_name='res.partner',
    )    
    property_type = fields.Many2one(
        string='Property Type',
        comodel_name='estate.property.type',
    )
    property_tags = fields.Many2many(
        string='Property Tag',
        comodel_name='estate.property.tag',
        column1='property_tag_id',
        column2='property_id',
    )
    property_offer_ids = fields.One2many(
        string='Property Offer',
        comodel_name='estate.property.offer',
        inverse_name='property_id',
    )

    total_area = fields.Float(
        string='Total Area',
        compute='_sum_total_area',
        readonly=True,
    )
    @api.depends('living_area','garden_area')
    def _sum_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(
        string='Best Price',
        compute='_compute_best_price',
        readonly=True,
    )
    @api.depends('property_offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                record.best_price = max(record.property_offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        self.ensure_one()
        if self.garden and not self.garden_area:
            self.garden_area = 10
            self.garden_orientation = 'north'
        elif self.garden:
            self.garden_orientation = 'north'
        elif not self.garden:
            self.garden_area = 0
            self.garden_orientation = None

    @api.onchange('garden_area','living_area')
    def _onchange_area(self):
        self.ensure_one()
        if self.garden_area < 0 or self.living_area < 0:
            raise UserError(_("Check your area option."))
        
    def _check_property_state(self):
        return self.state
        
    def action_sold_property(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_("Canceled"))
        self.write({'state':'sold'})
        return True
    
    def action_cancel_property(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_('The property is canceled'))
        self.write({'state':'canceled'})
        return True
            
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError(_("The selling price should be larger than 90% of the expected price."))
            
    @api.onchange('property_offer_ids')
    def _onchange_offer_ids(self):
        self.ensure_one()
        if len(self.property_offer_ids) > 0:
            self.state = 'offer_received'
            if 'accepted' in self.property_offer_ids.mapped('status'):
                self.state = 'offer_accepted'
        elif len(self.property_offer_ids) == 0 and self.state not in ('sold', 'canceled'):
            self.state = 'new'

    @api.ondelete(at_uninstall=False)
    def _unlink_property_not_new(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError(_('Can not delete the record with state%s' % record.state))
            