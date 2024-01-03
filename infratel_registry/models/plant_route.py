# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import api, fields, models

class PlantRoute(models.Model):
    _name = "plant.route"
    _description = "Plant route"
    
    name = fields.Char(string="Codice tratta", required=True)
    a_point = fields.Char(string="Punto A", required=True)
    z_point = fields.Char(string="Punto Z", required=True)
    node_code = fields.Char(string="Codice nodo", required=True)
    route_length = fields.Char(string="Lunghezza tratta", required=True)
    tavola = fields.Char(string="Tavola")
    from_street = fields.Char(string="Da Via/Civico")
    to_street = fields.Char(string="A Via/Civico")
    lat_value = fields.Char(string="Latitudine")
    long_value = fields.Char(string="Longitudine")
    note = fields.Text(string="Note")
    