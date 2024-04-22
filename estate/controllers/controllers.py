from odoo import http
from odoo.http import request, route

class EstateCounter(http.Controller):
    @http.route(['/estate_counter'], type='http', auth='public')
    def show_counter(self):
        """
        Show the Counter
        """
        return request.render('estate.Counter')