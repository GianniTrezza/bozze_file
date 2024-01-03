# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    infr_contact_type = fields.Selection([
        ('operatore', 'Operatore'),
        ('fornitore', 'Fornitore')
        ], string="Tipo contatto")
    operatore_enabled = fields.Boolean(string="Abilitato")
    active_framework_agreement = fields.Boolean(string="Accordo quadro attivo",
        compute='_compute_active_framework_agreement', store=True)
    email_pec = fields.Char(string="E-mail PEC")
    framework_agreement_ids = fields.One2many('framework.agreement', 'partner_id', string="Accordi quadro")
    framework_agreement_count = fields.Integer("Framework Count",
        compute="_compute_framework_agreement_count", store=True)

    
    @api.depends("framework_agreement_ids")
    def _compute_framework_agreement_count(self):
        for r in self:
            r.framework_agreement_count = len(r.framework_agreement_ids)

    @api.depends('framework_agreement_ids','framework_agreement_ids.state')
    def _compute_active_framework_agreement(self):
        """
        Used to compute 'active_framework_agreement' field
        base on 'framework_agreement_ids' state
        """
        for r in self:
            if r.framework_agreement_ids.filtered(lambda x: x.state == 'valid'):
                r.active_framework_agreement = True
            else:
                r.active_framework_agreement = False


    def action_view_partner_framework_agreement(self):
        for r in self:
            return {
                "name": "Accordi quadro",
                "type": "ir.actions.act_window",
                "view_mode": "tree,form",
                # "views": [(False, 'tree'), (False, 'form')],
                'res_model': 'framework.agreement',
                'domain': [('partner_id', '=', r.id)],
                'context': {'default_partner_id': r.id},
            }
