# -*- coding: utf-8 -*-
{
    'name': "sale_extend",

    'summary': "拓展销售模块的功能",

    'description': """
        为了在订单中除了主要负责人外，其余的客户一起加入，设置字段
    """,

    'author': "Enish",
    'website': "https://www.github.com/Enishk",

    'category': 'Sale',
    'version': '0.1',


    'depends': ['base', 'sale'],


    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'wizard/order_other_customer.xml',
    ],
    # only loaded in demonstration mode
    'license': 'LGPL-3',
}

