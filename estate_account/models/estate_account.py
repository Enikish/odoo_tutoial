# -*- coding: utf-8 -*-

from odoo import models, fields, api



MOVE_TYPE = [
    ('entry', 'Journal Entry'),
    ('out_invoice', 'Customer Invoice'),
    ('out_refund', 'Customer Credit Note'),
    ('in_invoice', 'Vendor Bill'),
    ('in_refund', 'Vendor Credit Note'),
    ('out_receipt', 'Sales Receipt'),
    ('in_receipt', 'Purchase Receipt'),
]


class estate_account(models.Model):
    _name = 'estate.account'
    _description = 'estate_account.estate_account'

    partner_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner',
        )    
    
    move_type = fields.Selection(
        string='Move Type',
        selection=MOVE_TYPE,
        store=True,
        required=True,
        default='entry',
    )

    journal_id = fields.Many2one(
        string='Accounting Journal',
        comodel_name='account.journal',
    )


