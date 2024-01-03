# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import fields, models

class InfSlaPolicyLabel(models.Model):
    _name = "inf.sla.policy.label"
    _description = "SLA Policy Label"

    name = fields.Char(string="Nome", required=True)

class InfSlaPolicy(models.Model):
    _name = "inf.sla.policy"
    _description = "SLA Policy"

    name = fields.Char(string="Titolo", required=True)
    description = fields.Text(string="Descrizione")
    sla_label_ids = fields.Many2many('inf.sla.policy.label', string="Etichette")
    sla_timing = fields.Integer(string="Tempistica", required=True)
    unit = fields.Selection([
        ('day', 'giorno'),
        ('month', 'mese'),
        ('year', 'anno')
    ], string="Unità di misura", required=True)
