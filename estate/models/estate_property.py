from odoo import models, fields, api, _
from odoo.exceptions import UserError

GARDEN_ORIENTATION = [('north', 'North'),
                      ('south', 'South'),
                      ('east', 'East'),
                      ('west', 'West'),
                      ]

STATE = [
    ('new', 'New'),
    ('offer', 'Offer'),
    ('received', 'Received'),
    ('offer accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled'),
]

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

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
        ondelete='cascade',
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
            return {'warning': {
                'title':_('Warning'),
                'message':('Please check your area option.')
            }}
        
    def _check_property_state(self):
        return self.state
        
    def action_sold_property(self):
        self.ensure_one()
        if self.state == 'canceled':
            return {'warning':{
                    'title':_('Warning'),
                    'message':('Canceled property can not be sold.')
                }
            }
        self.state = 'sold'
        return True
    
    def action_cancel_property(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_('The property is canceled'))
            return {
                'warning':{
                    'title':_('Warning'),
                    'message':('The property is already canceled.')
                }
            }
        # elif self.state == 'sold':
        #     return {
        #         'warning':{
        #             'title':_('Warning'),
        #             'message':('The property is already sold.')
        #         }
        #     }
        self.state = 'canceled'
        return True
            
    