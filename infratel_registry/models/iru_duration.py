# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import models, fields, api

class IruDuration(models.Model):
    _name = "iru.duration"
    _description = "Iru duration"
    
    name = fields.Char(string="Tipologia", required=True)
