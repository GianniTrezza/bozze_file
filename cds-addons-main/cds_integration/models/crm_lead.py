# Copyright 2023 Raffaele Amalfitano

from odoo import _, api, fields, models 

class CrmLead(models.Model):
    _inherit = "crm.lead"

    cds_transition_path_id = fields.Many2one('cds.transition.path',
        string="Percorso transizione")
    cds_service_type_id = fields.Many2one('cds.service.type',
        string="Servizio")
    cds_technological_area_ids = fields.Many2many('cds.technological.area',
        string="Aree tecnologiche")
    cds_application_scope_ids = fields.Many2many('cds.application.scope',
        string="Ambiti applicazione")
    cds_application_sector_ids = fields.Many2many('cds.application.sector',
        string="Settori applicazione")
    cds_ris3_area_ids = fields.Many2many('cds.ris3.area',
        string="Aree specializzazione RIS3")
    cds_trl_data_ids = fields.Many2many('cds.trl.data',
        string="Dati TRL")

    # matching
    product_matched_ids = fields.Many2many('product.template', string="Servizi matchati")

    def action_service_matching(self):
        """
        Action button method used to compile 'product_matched_ids'
        with matched services
        """
        # used to call the defined general methods
        cds_lib = self.env['cds.lib'].sudo()
        # apply matching method
        for record in self:
            record.product_matched_ids = False
            cds_lib.service_matching(record, record.cds_service_type_id)