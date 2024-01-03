# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import api, fields, models 

class FrameworkAgreement(models.Model):
    _inherit = 'framework.agreement'

    # foreign key to the res.partner model;
    # on partner_id remove, record with this foreign key will be deleted
    partner_id = fields.Many2one('res.partner', string="Contatto associato",
        required=True, ondelete='cascade')
    contact_type_rel = fields.Selection(related='partner_id.infr_contact_type',
        string="Tipo contatto")