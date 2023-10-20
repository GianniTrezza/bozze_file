# Copyright 2023 Raffaele Amalfitano

from odoo import _, api, fields, models 

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_solver = fields.Boolean(string="È un solver", default=False)
    is_seeker = fields.Boolean(string="È un seeker", default=False)