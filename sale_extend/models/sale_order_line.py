from odoo import fields, models, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    currency_id = fields.Many2one(comodel_name='res.currency', related='order_id.currency_id')
    cost = fields.Monetary(string='成本', currency_field='currency_id')
    benefit = fields.Monetary(string='利润', currency_field='currency_id', compute='_compute_benefit')

    @api.depends('cost', 'price_subtotal')
    def _compute_benefit(self):
        for line in self:
            line.benefit = line.price_subtotal - line.cost


    