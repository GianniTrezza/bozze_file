# Copyright 2023 Raffaele Amalfitano

from odoo import _, api, fields, models 


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # cds_data
    supplier_id = fields.Many2one('res.partner', string="Fornitore", copy=False)
    cds_service_benefits = fields.Text(string="Benefici", copy=False)
    # cds_transition_path_ids = fields.Many2many('cds.transition.path', string="Percorsi transizione")
    cds_service_type_id = fields.Many2one('cds.service.type', string="Tipologie servizio")
    cds_technological_area_ids = fields.Many2many('cds.technological.area', string="Aree tecnologiche")
    cds_application_scope_ids = fields.Many2many('cds.application.scope', string="Ambiti applicazione")
    cds_application_sector_ids = fields.Many2many('cds.application.sector', string="Settori applicazione")
    cds_ris3_area_ids = fields.Many2many('cds.ris3.area', string="Aree specializzazione RIS3")
    cds_trl_data_ids = fields.Many2many('cds.trl.data', string="Dati TRL")
