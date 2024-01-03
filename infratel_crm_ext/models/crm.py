# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = "crm.lead"

    region = fields.Char(string="Regione")
    municipality = fields.Char(string="Comune")

    project_request_id = fields.Many2one('project.request', string="Progetto relativo a")
    infr_order = fields.Char(string="Commessa")
    framework_agreement_id = fields.Many2one('framework.agreement', string="Accordo quadro",
        help="""Accordo quadro legato al cliente della richiesta.""")
    filtered_framework_agreement_ids = fields.Many2many('framework.agreement',
        compute='_compute_filtered_framework_agreement_ids')
    cig = fields.Char(string="CIG")
    cup = fields.Char(string="CUP")
    request_type = fields.Selection([
        ('backhualing', 'Backhualing'),
        ('access_network', 'Rete di accesso')
        ], string="Tipo richiesta")

    # contact referent data
    contact_referent_id = fields.Many2one('res.partner', string="Referente",
        help="""Contatto operatore, figlio del contatto 'Cliente'.""")
    email_rel = fields.Char(related='contact_referent_id.email', string="E-mail")
    pec_rel = fields.Char(related='contact_referent_id.email_pec', string="E-mail PEC")
    phone_rel = fields.Char(related='contact_referent_id.phone', string="Telefono")
    
    joint_testing = fields.Boolean(string="Collaudo congiunto")
    
    # lin to the crm.request.line model
    crm_request_line_ids = fields.One2many('crm.request.line', 'crm_id', string='Request line')

    def _compute_filtered_framework_agreement_ids(self):
        """
        Retrieve valid agreements related to the
        CRM 'partner_id' field
        """
        for r in self:
            if r.partner_id and r.partner_id.framework_agreement_ids:
                r.filtered_framework_agreement_ids = [(6, 0, r.partner_id.framework_agreement_ids.filtered(lambda x: x.state == 'valid').ids)]
            else:
                r.filtered_framework_agreement_ids = False


class CrmRequestLine(models.Model):
    _name = "crm.request.line"
    _description = "Crm request line"

    # foreign key to the crm.lead model;
    # on crm_id remove, record with this foreign key will be deleted
    crm_id = fields.Many2one('crm.lead', string='Request', required=True, ondelete='cascade')

    plant_route_id = fields.Many2one('plant.route', string="Tratta", required=True)
    route_length_rel = fields.Char(related='plant_route_id.route_length', string="Lunghezza tratta")
    product_template_id = fields.Many2one('product.template', string="Prodotto/Servizio", required=True)
    quantity = fields.Float(string="Quantità", required=True)
    uom_id = fields.Many2one('uom.uom', string="Unità di misura")
    iru_duration_id = fields.Many2one('iru.duration', string="Durata IRU")
    
    