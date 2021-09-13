# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class MarketPlaceReportLine(models.Model):
    _name = 'report.market.place'
    _auto = False
    _description = 'This is the lines in the market place report'
    

    product_id = fields.Many2one('product.product','Product',readonly=True)
    company_id = fields.Many2one('res.company','Compañía',readonly=True)
    sale_order_id = fields.Many2one('sale.order','Número de Pedido',readonly=True)
    #sale_order_name = fields.Char('Nombre de la Orden de Venta',readonly=True)
    product_uom_qty = fields.Float('Cantidad',readonly=True)
    qty_invoiced = fields.Float('Facturado',readonly=True)
    qty_delivered = fields.Float('Entregado',readonly=True)
    price_total = fields.Float('Valor Venta',readonly=True)
    service_order = fields.Char('Orden de Servicio',readonly=True)
    default_code = fields.Char('Referencia Interna Odoo',readonly=True)
    sale_type_id = fields.Many2one('sale.type', 'Tipo de Venta')
    date_order = fields.Datetime('Fecha del Pedido')
    currency_id = fields.Many2one('res.currency', 'Moneda')
    partner_id = fields.Many2one('res.partner', 'Cliente Odoo')
    order_final_partner_raw = fields.Char('Cliente Final')
    market_place_id = fields.Many2one('sale.market.place', 'Market Place')
    sku = fields.Char('SKU Market Place')
    
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_market_place')
        query = """
        CREATE or REPLACE VIEW report_market_place AS(
        
        select 
        row_number() OVER (ORDER BY sol.id) as id,
        so.company_id as company_id,
        sol.product_id as product_id,
        sol.order_id as sale_order_id,
        --so.name::text as sale_order_name,
        sol.product_uom_qty,
        sol.qty_invoiced,
        sol.qty_delivered,
        pro.default_code,
        sol.price_total,
        sol.service_order,
        so.date_order,
        mp.id as market_place_id,
        so.partner_id,
        so.currency_id,
        so.sale_type_id as sale_type_id,
        ppmp.sku,
        sol.order_final_partner_raw
        from sale_order_line sol
        left join sale_order so on so.id = sol.order_id
        left join product_product pro on pro.id = sol.product_id
        left join sale_market_place mp on mp.partner_id = so.partner_id
        left join product_product_market_place ppmp on ppmp.product_id = sol.product_id and ppmp.market_place_id = mp.id
        --left join res_company co on co.id = so.company_id
        where 1=1
        );
        """
        self.env.cr.execute(query)
        #(select to_char(mp.date_planned_start,'mm')) as month,