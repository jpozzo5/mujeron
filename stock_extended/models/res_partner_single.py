# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class ResPartnerSingle(models.Model):
    _name = 'res.partner.single'
    _description = 'Entidad Terceros Solo Nombre'
    #_order = 'code,mame'
    #_sql_constraints = [('code_mame_check', 'UNIQUE(code,name)', _("The code have to unique"))]
    
    #code = fields.Char('Code', required=True, size=2)
    name = fields.Char('Nombre del Cliente Final', track_visibility='onchange')
    active = fields.Boolean(default=True, help="\
        The active field allows you to hide the class without removing it.", track_visibility='onchange')