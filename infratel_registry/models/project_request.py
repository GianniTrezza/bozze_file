# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import fields, models

class ProjectRequest(models.Model):
    _name = "project.request"
    _description = "Project request"

    name = fields.Char(string="Nome", required=True)