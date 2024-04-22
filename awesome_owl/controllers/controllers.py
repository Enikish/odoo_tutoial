from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.playground')
    
class OwlCounter(http.Controller):
    @http.route(['/awesome_owl/counter'], type='http', auth='public')
    def show_counter(self):
        return request.render('awesome_owl.Counter')