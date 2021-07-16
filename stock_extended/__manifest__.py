# -*- coding: utf-8 -*-
{
    'name': "Stock Mujeron Extended",

    #'summary': "Stock Mujeron Extended",

    'description': "Módulo para extender la funcionalidad de inventarios en Mujeron, desde su venta hasta la factura",

    'author': "Todoo SAS",
    'contributors': ['Jhair Escobar je@todoo.co'],
    'website': "http://www.todoo.co",

    'category': 'Sales/Sales',
    'version': '14.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/market_place.xml',
        'views/sale_market_place_view.xml',
        'views/sale_type_view.xml',
        'views/sale_invoice_method_view.xml',
        'views/sale_market_place_commission_view.xml',
        'views/res_partner_view.xml',
        #'views/res_partner_single_view.xml',
        'views/sale_order_view.xml',
        'views/product_product_view.xml',
        'views/report_view.xml',
        #'views/product_product_market_place_view.xml',
        #'views/template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    
    'installable': True,
    'application': True,
}
