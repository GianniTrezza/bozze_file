# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    project_request_id = fields.Many2one('project.request', string="Progetto relativo a")
    infr_order = fields.Char(string="Commessa")
    framework_agreement_id = fields.Many2one('framework.agreement', string="Accordo quadro",
        help="""Accordo quadro legato al fornitore dell'ordine di acquisto""")
    filtered_framework_agreement_ids = fields.Many2many('framework.agreement',
        compute='_compute_filtered_framework_agreement_ids')
    sla_policy_id_rel = fields.Many2one(related='framework_agreement_id.sla_policy_id', string="Politica SLA")
    cig = fields.Char(string="CIG")
    cup = fields.Char(string="CUP")
    request_type = fields.Selection([
        ('backhualing', 'Backhualing'),
        ('access_network', 'Rete di accesso')
        ], string="Tipo richiesta")

    # contact referent data
    contact_referent_id = fields.Many2one('res.partner', string="Referente")
    email_rel = fields.Char(related='contact_referent_id.email', string="E-mail")
    pec_rel = fields.Char(related='contact_referent_id.email_pec', string="E-mail PEC")
    phone_rel = fields.Char(related='contact_referent_id.phone', string="Telefono")

    joint_testing = fields.Boolean(string="Collaudo congiunto")

    expiration_date = fields.Date(string="Deadline")
    actual_delivery_date = fields.Date(string="Data di consegna effettiva")

    # users related to specific groups
    delivery_employee_id = fields.Many2one('res.users',  string="Dipendente delivery")
    works_director_id = fields.Many2one('res.users', string="Direttore lavori")
    execution_security_coordinator_id = fields.Many2one('res.users', string="Coordinatore sicurezza esecuzione")
    design_safety_coordinator_id = fields.Many2one('res.users', string="Coordinatore sicurezza progettazione")

    def _compute_filtered_framework_agreement_ids(self):
        """
        Retrieve valid agreements related to the
        purchase order 'partner_id' field
        """
        for r in self:
            if r.partner_id and r.partner_id.framework_agreement_ids:
                r.filtered_framework_agreement_ids = [(6, 0, r.partner_id.framework_agreement_ids.filtered(lambda x: x.state == 'valid').ids)]
            else:
                r.filtered_framework_agreement_ids = False
    
    def validation_action(self):
        return True

    def approval_action(self):
        return True

    def signature_action(self):
        return True

    def suspend_action(self):
        return True

    def reactivate_action(self):
        return True

    def new_order_creation_action(self):
        return True
    

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    plant_route_id = fields.Many2one('plant.route', string="Tratta")
    route_length_rel = fields.Char(related='plant_route_id.route_length', string="Lunghezza tratta")
