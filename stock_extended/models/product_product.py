# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_sku_ids = fields.One2many('product.product.market.place', 'product_id', string="SKU Market Place")
    
    
    
    def write(self, values):
        res = super(ProductProduct, self).write(values)
        for rec in self:
            mp_exist = None
            for sku in rec.product_sku_ids:
                mp_exist = self.env['product.product.market.place'].search([
                    ('market_place_id', '=', sku.market_place_id.id),
                    ('sku', '=', sku.sku),
                ])
                if len(mp_exist) > 1:
                    #raise ValidationError('El SKU: %s ya existe registrado para el Market Place: %s' % (mp_exist.sku, mp_exist.market_place_id.name))
                    raise ValidationError('El SKU: %s ya existe registrado para el Market Place: %s' % (sku.sku, sku.market_place_id.name))

        return res