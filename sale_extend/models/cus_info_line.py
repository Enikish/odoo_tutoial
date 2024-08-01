from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError

GENDER = [
    ('male', '男'),
    ('female', '女')
    ]

class CusInfoLine(models.Model):
    _name = 'cus.info.line'

    trip_group = fields.Many2one(comodel_name='sale.order', string='Trip Group')
    cus_info = fields.Many2one(comodel_name='res.partner', string='Customer Info')
    cus_id = fields.Char(string='身份证号', compute='_compute_cus_id')
    cus_name = fields.Char(string='姓名', compute='_compute_cus_name')
    cus_phone = fields.Char(string='电话', compute='_compute_cus_phone')
    cus_email = fields.Char(string='邮箱', compute='_compute_cus_email')
    cus_age = fields.Integer(string='年龄', compute='_compute_cus_age')
    cus_gender = fields.Selection(string='性别', 
                                  compute='_compute_cus_gender', 
                                  selection=GENDER)

    @api.depends('cus_info')
    def _compute_cus_id(self):
        for rec in self:
            rec.cus_id = rec.cus_info.id_card

    @api.depends('cus_info')
    def _compute_cus_name(self):
        for rec in self:
            rec.cus_name = rec.cus_info.name

    @api.depends('cus_info')
    def _compute_cus_phone(self):
        for rec in self:
            rec.cus_phone = rec.cus_info.phone


    @api.depends('cus_info')
    def _compute_cus_address(self):
        for rec in self:
            rec.cus_address = rec.cus_info.street

    @api.depends('cus_info')
    def _compute_cus_age(self):
        for rec in self:
            rec.cus_age = rec.cus_info.age
    
    @api.depends('cus_info')
    def _compute_cus_gender(self):
        for rec in self:
            rec.cus_gender = rec.cus_info.gender