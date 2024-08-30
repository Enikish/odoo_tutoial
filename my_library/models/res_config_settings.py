from odoo import models, api, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_self_borrow = fields.Boolean(string='Self borrow',
                                       implied_group='my_library.group_self_borrow')