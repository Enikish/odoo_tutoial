from odoo import models, fields, api, _


class OrderOtherCustomer(models.TransientModel):
    _name = 'order.other.customer'

    customers = fields.Many2many(comodel_name='res.partner',
                                 relation='order_other_customers',
                                 column1='order_wiz_id',
                                 column2='order_wiz_customer_id')
    
    order_id = fields.Many2one(comodel_name='sale.order',
                               string='跟团单号')


    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model', False)
        order_id = None
        if active_model == 'sale.order':
            order_id = self.env.context.get('active_id', False)
        res['order_id'] = order_id
        return res            
    
    def confirm_customers(self):
        cusInfoModel = self.env['cus.info.line']
        saleOrderModel = self.env['sale.order']
        order = False
        for wiz in self:
            sale_order = saleOrderModel.browse(wiz.order_id.id)
            for customer in wiz.customers:
                cus_info = cusInfoModel.create({
                    'trip_group': wiz.order_id.id,
                    'cus_info': customer.id,
                })
                sale_order.info_lines = [(4, cus_info.id)]
        return