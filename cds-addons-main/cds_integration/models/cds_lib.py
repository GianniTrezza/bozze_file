# Copyright 2023 Raffaele Amalfitano

from odoo import _, api, fields, models 

class CdsLib(models.Model):
    _name = "cds.lib"
    _description = "Cds Lib"

    def service_matching(self, crm_lead_obj, service_type_obj):
        # search products based on data specified on crm record.
        # search first by service type
        product_ids = self.env['product.template'].sudo().search([('cds_service_type_id', '=', service_type_obj.id)])
        first_level_prod_ids = product_ids
        # search by techn area
        second_level_prod_ids = self.env['product.template'].sudo()
        if crm_lead_obj.cds_technological_area_ids:
            for area in crm_lead_obj.cds_technological_area_ids:
                second_level_prod_ids |= first_level_prod_ids.filtered(lambda x: area in x.cds_technological_area_ids)
        # search by application scope
        third_level_prod_ids = self.env['product.template'].sudo()
        if crm_lead_obj.cds_application_scope_ids:
            for appl_scope in crm_lead_obj.cds_application_scope_ids:
                third_level_prod_ids |= second_level_prod_ids.filtered(lambda x: appl_scope in x.cds_application_scope_ids)
        # search by sector
        fourth_level_prod_ids = self.env['product.template'].sudo()
        if crm_lead_obj.cds_application_sector_ids:
            for sector in crm_lead_obj.cds_application_sector_ids:
                fourth_level_prod_ids |= third_level_prod_ids.filtered(lambda x: sector in x.cds_application_sector_ids)
        # search by ris3 area
        fifth_level_prod_ids = self.env['product.template'].sudo()
        if crm_lead_obj.cds_ris3_area_ids:
            for area in crm_lead_obj.cds_ris3_area_ids:
                fifth_level_prod_ids |= fourth_level_prod_ids.filtered(lambda x: area in x.cds_ris3_area_ids)
        # search by ris3 area
        sixth_level_prod_ids = self.env['product.template'].sudo()
        if crm_lead_obj.cds_trl_data_ids:
            for trl in crm_lead_obj.cds_trl_data_ids:
                sixth_level_prod_ids |= fifth_level_prod_ids.filtered(lambda x: trl in x.cds_trl_data_ids)
        
        if sixth_level_prod_ids:
            crm_lead_obj.product_matched_ids = [(6, 0, sixth_level_prod_ids.ids)]
        elif fifth_level_prod_ids:
            crm_lead_obj.product_matched_ids = [(6, 0, fifth_level_prod_ids.ids)]
        elif fourth_level_prod_ids:
            crm_lead_obj.product_matched_ids = [(6, 0, fourth_level_prod_ids.ids)]
        elif third_level_prod_ids:
            crm_lead_obj.product_matched_ids = [(6, 0, third_level_prod_ids.ids)]
        elif second_level_prod_ids:
            crm_lead_obj.product_matched_ids = [(6, 0, second_level_prod_ids.ids)]
        elif first_level_prod_ids:
            crm_lead_obj.product_matched_ids = [(6, 0, first_level_prod_ids.ids)]
        # else:
        #     print("Match non trovato!")

    def _missing_mandatory_data(self, text=False):
        args = {
            'success': False,
            'status': 422, # Unprocessable Entity
            'message': 'Missing mandatory data!'
        }
        if text:
            args['message'] += " {}".format(text)
        return args

    def _not_found_data(self, text=False):
        args = {
            'success': False,
            'status': 404,
            'message': ''
        }
        args['message'] += "{}".format(text)
        return args

    def _method_not_allowed(self, text=False):
        args = {
            'success': False,
            'status': 405,
            'message': ''
        }
        args['message'] += "{}".format(text)
        return args