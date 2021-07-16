# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class ProductProductMarketPlace(models.Model):
    _name = 'product.product.market.place'

    company_id = fields.Many2one('res.company', 'Compañia')
    product_id = fields.Many2one('product.product', 'Producto')
    market_place_id = fields.Many2one('sale.market.place', 'Market Place')
    sku = fields.Char('SKU')
    
    