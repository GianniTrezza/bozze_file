# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import api, fields, models


class CdsTransitionPath(models.Model):
    _name = "cds.transition.path"
    _description = "Cds transition path"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nome", required=True, tracking=True)


class CdsServiceType(models.Model):
    _name = "cds.service.type"
    _description = "Cds service type"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nome", required=True, tracking=True)

class CdsTechnologicalArea(models.Model):
    _name = "cds.technological.area"
    _description = "Cds technological area"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nome", required=True, tracking=True)

class CdsApplicationScope(models.Model):
    _name = "cds.application.scope"
    _description = "Cds application scope"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nome", required=True, tracking=True)


class CdsApplicationSector(models.Model):
    _name = "cds.application.sector"
    _description = "Cds application sector"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nome", required=True, tracking=True)


class CdsRis3Area(models.Model):
    _name = "cds.ris3.area"
    _description = "Cds ris3 area"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nome", required=True, tracking=True)


class CdsTrlData(models.Model):
    _name = "cds.trl.data"
    _description = "Cds trl data"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nome", required=True, tracking=True)