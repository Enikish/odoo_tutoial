from os.path import join
from odoo import models, fields, api, _
from odoo.exceptions import UserError

EXPORTS_DIR = '/src/exports'

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def export_stock_level(self, stock_location):
        import pdb;pdb.set_trace()
        products = self.with_context(
            location=stock_location.id,
        ).search([])
        products = products.filtered('qty_available')
        fname = join(EXPORTS_DIR, 'stock_level.txt')   
        try:
            with open(fname, 'w') as fobj:
                for prod in products:
                    fobj.write('%s\t%f\n' % (prod.name, prod.qty_available))
        except IOError:
            raise UserError(_('Unable to save file'))
    
