# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleMarketPlaceCommission(models.Model):
    _name = 'sale.market.place.commission'
    _description = 'Comisiones para el Market Place'
    
    name = fields.Char(compute="_compute_sale_market_place_name", store=True, readonly=True)
    active = fields.Boolean(default=True, help="\
        The active field allows you to hide the class without removing it.", required=True, track_visibility='onchange')
    company_id = fields.Many2one('res.company', 'Compañía', required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', 'Cliente', tracking=True, required=True, help='Cliente en Odoo', copy=False)
    market_place_id = fields.Many2one('sale.market.place', 'Market Place', required=True, tracking=True, help='Seleccione el Market Place')
    sale_type_id = fields.Many2one('sale.type', 'Tipo de Venta', tracking=True, required=True, help='Seleccione el Tipo de Venta')
    sale_invoice_method_id = fields.Many2one('sale.invoice.method', 'Metodo de Facturación', required=True, tracking=True, help='Seleccione el Metodo de Facturación')
    commission_mp_type = fields.Selection([('percentage', 'Porcentaje'), ('fixed', 'Valor Fijo')], 'Tipo de Comisión para el Market Place', 
                                          help='Seleccione si la comisión para el market place está expresado en porcentaje o un valor fijo')
    bonuses_type = fields.Selection([('percentage', 'Porcentaje'), ('fixed', 'Valor Fijo')], 'Tipo de Bonificación', 
                                    help='Seleccione si la bonificación está expresada en porcentaje o un valor fijo')
    commission_mp = fields.Integer('Comisión para el Market Place', help='Comisión para el Market Place')
    bonuses = fields.Integer('Bonificación', help='Bonificación')
    
    
    @api.depends(
        'active',
        'company_id',
        'partner_id',
        'market_place_id',
        'sale_type_id',
        'sale_invoice_method_id',
        'commission_mp_type',
        'bonuses_type',
        'commission_mp',
        'bonuses'
    )
    def _compute_sale_market_place_name(self):
        str = ' - '
        seq = [
            self.company_id.name,
            self.partner_id.name or '',
            self.market_place_id.name or '',
            self.sale_type_id.name or '',
            self.sale_invoice_method_id.name or ''
        ]
        self.name = str.join( seq )