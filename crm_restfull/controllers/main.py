# -*- coding: utf-8 -*-

from odoo import http,_
import json
from odoo.http import Response, request
# from .Shemas.schemaJson import Shema  aun no va hay que instalar la libreria.
import logging
_logger = logging.getLogger(__name__)

class MyController(http.Controller):
    """
        -Al recibir los datos del cliente validamos si el cliente existe en nuestra bases de datos,
        luego verificamos si se ha realizado alguna venta anteriormente si existe almenos 1 venta se
        creara como oportunidad.(LISTO-DEV)

        -Al recibir los datos del cliente validamos si el cliente existe en nuestra bases de datos ,
        si existe + de 1 cliente con los mismo datos de busqueda (tlf,email,etc.) se buscaran todos los peditos
        de ventas de estos cliente y se tomara el cliente con la venta mas reciente.(LISTO-DEV)
        ---------------------------------------------------------------------------------------------------------
        -Al realizar los procesos anteriores si el cliente no tiene ventas crear como oportunidad.(LISTO-DEV)
        -Validar Cuando el partner no existe en la bases de datos odoo retornar el error.(LISTO-DEV)
        -No tienen pedidos de ventas y existe mas de 1 cliente con los mismos datos ,crear la iniciatica con el ultimo cliente creado.(LISTO QA)


    """

    def get_partner(self,phone,mobile,email):
        numberCommun = True
        partner_id = request.env['res.partner'].sudo().search([
                '|','|',('phone','=',phone),
                    ('mobile','=',mobile),
                    ('email','=',email)
        ])
        if len(partner_id) == 1:
            return partner_id , numberCommun
        elif len(partner_id) > 1:
            """
                Aqui si existe varios cliente con el mismo correo ó numero telefonico realizara la busqueda de los pedidos de ventas de todoos ellos 
                y se creara el lead con el cliente que se le vendio a una fecha mas reciente.
            """
            partners = [partner.id for partner in partner_id ]
            sale_order_ids = request.env['sale.order'].sudo().search([('partner_id','in',partners)],order="date_order desc",limit=1)
            if sale_order_ids:
                numberCommun = False 
                return sale_order_ids.partner_id , numberCommun
            else:
                #Si no tiene tiene ventas se toma el ultimo vendedor creado en odoo par acrear la iniciativa
                partner_sort = partner_id.sorted(key=lambda r: r.create_date) 
                return partner_sort , numberCommun

        else:# no encontro el cliente 
            return None ,None

    def get_seller(self,email):
        seller_id = request.env['res.users'].sudo().search([('email','=',email)],limit=1)#siempre toma el primero
        if seller_id:
            return seller_id , False
        else:
            return None , True

    @http.route(['/get_cliente_crm'], 
                type='json', auth='public', methods=['POST'], csrf=False)
    def get_cliente_crm(self,**post):
        # a = Shema().validateJson(request.httprequest.data)
        # logging.info(a)
        ctx_respont = {}
        if request.httprequest.data:
            ctx_consult = json.loads(request.httprequest.data)
            partner_id ,numberCommun = self.get_partner(ctx_consult['phone'],ctx_consult['mobile'],ctx_consult['email'])
            if partner_id:
                sale_order = request.env['sale.order'].sudo().search([('partner_id','=',partner_id.id)],order="date_order")
                if sale_order:#Si existe el cliente y ventas Crear oportunidad
                    seller_id , error_seller= self.get_seller(ctx_consult['data_seller']['email_seller'])
                    if error_seller:
                        ctx_respont ={'results':{
                                    'new_leads_id_odoo':'',
                                },
                                'details':{
                                    'message':'Fue encontrado 1 solo cliente en odoo y tiene pedidos de ventas .' if numberCommun else  'Fue encontrado mas de 1 cliente  y tiene pedidos de ventas .',
                                    'errors':['El vendedor {} no existe en la BD de odoo.'.format(ctx_consult['data_seller']['email_seller'])],
                                }
                            }
                    else:#si no existe ningun error al buscar el vendedor creamos el lead.
                        stage_id = request.env['crm.stage'].sudo().search([('name','=','New')])
                        ctx_create = {
                            'stage_id':stage_id.id,
                            'partner_id':partner_id.id,
                            'user_id':seller_id.id,
                            'name':ctx_consult['name_lead'],
                            'active':True
                        
                        }
                        lead_id = request.env['crm.lead'].sudo().create(ctx_create)#se crea Oportunidad.
                        ctx_respont ={'results':{
                                    'new_leads_id_odoo':lead_id.id,
                                },
                                'details':{
                                    'message':'Fue encontrado 1 solo cliente en odoo y tiene pedidos de ventas .' if numberCommun else  'Fue encontrado mas de 1 cliente  y tiene pedidos de ventas ,El lead fue creado con Exito.',
                                    'errors':[],
                                }
                            }
                else:#iniciativas 
                    seller_id , error_seller= self.get_seller(ctx_consult['data_seller']['email_seller'])
                    if error_seller:
                        ctx_respont ={'results':{
                                    'new_leads_id_odoo':'',
                                },
                                'details':{
                                    'message':'Fue encontrado 1 solo cliente en odoo y (No) tiene pedidos de ventas .' if numberCommun else  'Fue encontrado mas de 1 cliente  y (No) tiene pedidos de ventas .',
                                    'errors':['El vendedor {} no existe en la BD de odoo.'.format(ctx_consult['data_seller']['email_seller'])],
                                }
                            }
                    else:
                        stage_id = request.env['crm.stage'].sudo().search([('name','=','New')])
                        ctx_create = {
                            'stage_id':stage_id.id,
                            'partner_id':partner_id.id,
                            'user_id':seller_id.id,
                            'name':ctx_consult['name_lead'],
                            'active':True,
                            'type':'lead'
                        
                        }
                        lead_id = request.env['crm.lead'].sudo().create(ctx_create)#se crea iniciativa.
                        ctx_respont ={'results':{
                                    'new_leads_id_odoo':lead_id.id,
                                },
                                'details':{
                                    'message':'Fue encontrado 1 solo cliente en odoo y (No) tiene pedidos de ventas .La Iniciativa fue creado con Exito.' if numberCommun else  'Fue encontrado mas de 1 cliente  y (No) tiene pedidos de ventas ,La Iniciativa fue creado con Exito.',
                                    'errors':[],
                                }
                            }
            else:
                #si no existe el cliente
                ctx_respont ={'results':{
                                    'new_leads_id_odoo':'',
                                },
                                'details':{
                                    'message':'-',
                                    'errors':["El Cliente {} no existe en la BD de odoo fue . la busqueda se realizo por  : (telefono:{} /  mobil:{} / email:{}).".format(ctx_consult['name'],ctx_consult['phone'],ctx_consult['mobile'],ctx_consult['email'])
                                        
                                    ],
                                }
                            }                    
        else:
            ctx_respont = {
                'results':{
                    'message':"Error ,nada que consultar.",
                }
            }
        return json.dumps(ctx_respont)


    @http.route(['''/test/<int:order_id>''',]
        , auth='public',methods=['GET'],website=True)
    def test(self,order_id=None ,**args):
        _logger.warn("GET")
        _logger.warn(order_id)
        _logger.info(args)
        output = {
            'results':{
                'code':200,
                'message':'OK',
                'order_id':order_id
            }
        }
        logging.info(request.httprequest.data)

        return json.dumps(output)



