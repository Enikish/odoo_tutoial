from datetime import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.exceptions import UserError

GENDER = [
    ('male', '男'),
    ('female', '女')
    ]
    


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    id_card = fields.Char(string='身份证')
    age = fields.Integer(string='年龄', compute='_compute_age')
    gender = fields.Selection(selection=GENDER, string='性别', compute='_compute_gender')


    @api.depends('id_card')
    def _compute_age(self):
        for record in self:
            id_card = record.id_card
            if id_card and len(id_card) == 18:
                try:
                    birth_date_str = id_card[6:14]
                    birth_date = datetime.strptime(birth_date_str, '%Y%m%d')
                except ValueError as e:
                    raise UserError(_('%s身份证号格式错误, 详细信息:%s' % (record.name, e)))
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day)< (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0
    
    @api.depends('id_card')
    def _compute_gender(self):
        for record in self:
            id_card = record.id_card
            if id_card and len(id_card) == 18:
                gender_factor = int(record.id_card[-2]) % 2
                if gender_factor == 1:
                    record.gender = 'male'
                else:
                    record.gender = 'female'
            else:
                record.gender = ''
            

    @api.onchange('id_card')
    def _onchange_id_card_format(self):
        import re
        pattern = r'^[1-9][0-9]{16}[0-9Xx]'
        try:
            id_res = re.search(pattern, self.id_card)
            if id_res:
                self.id_card = id_res.string
            else:
                raise UserError(_('%s的身份证号格式不正确, %s, %s') % (self.name, id_res, self.id_card))
        except Exception as e:
            pass
            
