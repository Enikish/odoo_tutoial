from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    info_lines = fields.One2many(comodel_name='cus.info.line',
                                 string='Other members',
                                 inverse_name='trip_group',
                                 )
    
    currency_id = fields.Many2one(comodel_name='res.currency', 
                                  string='Currency', 
                                  required=True, 
                                  default=lambda self: self.env.company.currency_id)
    
    amount_cost = fields.Monetary(string='成本', compute='_compute_benefit')
    benefit = fields.Monetary(string='利润', compute='_compute_benefit')



    @api.depends('order_line.cost', 'amount_total')
    def _compute_benefit(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            amount_cost = sum(order_lines.mapped('cost'))
            order.amount_cost = amount_cost
            order.benefit = order.amount_total - amount_cost


