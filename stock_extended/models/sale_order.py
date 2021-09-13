# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_type_id = fields.Many2one('sale.type', 'Tipo de Venta')
    partner_single_ok = fields.Boolean(string='Cliente Final de Contactos')
    service_order_all = fields.Char('Ordenes de Servicio', compute="_compute_service_order_all", store=True)
    partner_marketplace_ok = fields.Boolean(string='Es Cliente Marketplace?', compute="_compute_partner_marketplace_ok")
    
    
    @api.onchange('partner_id')
    def _compute_partner_marketplace_ok(self):
        for rec in self:
            rec.partner_marketplace_ok = False
            partner_obj = self.env['sale.market.place'].search([('partner_id', '=', rec.partner_id.id)])
            if partner_obj:
                rec.partner_marketplace_ok = True
        
        
    
    @api.depends('order_line')
    def _compute_service_order_all(self):
        for rec in self:
            str = ','
            seq = []
            rec.service_order_all = ''
            for line in rec.order_line.mapped('service_order'):
                if line:
                    seq.append(line)
            if seq:
                rec.service_order_all = str.join( seq )
    
    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        list_ctl = []
        if 'order_line' in values and values['order_line']:
            for line in values['order_line']:
                if 'service_order' in line[2] and line[2]['service_order'] and res.id:
                    line_obj = self.env['sale.order.line'].search([
                        ('service_order', '=', str(line[2]['service_order'])),
                        ('order_id', '!=', res.id)
                    ], limit=1)
                    if line_obj:
                        raise ValidationError(
                            'La Order de Servicio %s no puede estar repetida. Ya se encuentra registrada en la orden %s' % (line[2]['service_order'], line_obj.order_id.name))
                    if line[2]['service_order'] not in list_ctl:
                        list_ctl.append(line[2]['service_order'])
                    else:
                        raise ValidationError(
                            'La Order de Servicio %s no puede estar repetida. Ya se encuentra registrada en esta misma orden' % (line[2]['service_order']))
        return res
    

    def write(self, values):
        res = super(SaleOrder, self).write(values)
        list_ctl = []
        for line in self.order_line.filtered(lambda x: x.service_order).mapped('service_order'):
            line_obj = self.env['sale.order.line'].search([
                ('service_order', '=', line),('order_id', '!=', self.id)
            ], limit=1)
            if line_obj:
                raise ValidationError(
                    'La Order de Servicio %s no puede estar repetida. Ya se encuentra registrada2 en la orden %s' % (line, line_obj.order_id.name))
            if line not in list_ctl:
                list_ctl.append(line)
            else:
                raise ValidationError(
                    'La Order de Servicio %s no puede estar repetida. Ya se encuentra registrada en esta misma orden' % (line))
        return res
    
    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    order_final_single_partner = fields.Char(string='Cliente Final solo nombre', readonly=False)
    order_final_partner_id = fields.Many2one('res.partner', string='Cliente Final Contactos', readonly=False)
    service_order = fields.Char('Orden de Servicio')
    partner_single_ok = fields.Boolean(related='order_id.partner_single_ok', string='Cliente Final de Contactos',readonly=True)
    partner_marketplace_ok = fields.Boolean(related='order_id.partner_marketplace_ok', string='Es Cliente Marketplace?',readonly=True)
    order_final_partner_raw = fields.Char('Cliente Final', compute="_compute_order_final_partner_raw", store=True)
    
    @api.depends('order_final_single_partner', 'order_final_partner_id', 'partner_single_ok')
    def _compute_order_final_partner_raw(self):
        for rec in self:
            if rec.partner_single_ok:
                rec.order_final_partner_raw = rec.order_final_partner_id.name
            else:
                rec.order_final_partner_raw = rec.order_final_single_partner
        
    
        
    