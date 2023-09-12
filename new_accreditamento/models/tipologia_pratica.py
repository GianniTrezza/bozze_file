# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class TipologiaPratica(models.Model):
    _name = 'hospital.tipologia_pratica'
    _description = "Tipo di Pratica d'Accreditamento"

    name = fields.Char(string='Nome', required=True)