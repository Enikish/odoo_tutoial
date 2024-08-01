# -*- coding: utf-8 -*-
{
    'name': "sale_extend",

    'summary': "拓展销售模块的功能",

    'description': """
        为了在订单中除了主要负责人外，其余的客户一起加入，设置字段
    """,

    'author': "Enish",
    'website': "https://www.github.com/Enishk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
}

