from odoo import models, fields, api,  _, Command



class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold_property(self):
        print('子类sold调用')
        account_move_params = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'journal_id': 1,
            'invoice_line_ids': [
                Command.create({
                    'name': 'VAT',
                    'quantity': 1,  
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': 'Extra Fee',
                    'quantity': 1,
                    'price_unit': 100,
                })
            ]
        }
        self.env['account.move'].create(account_move_params)
        return super().action_sold_property()
    