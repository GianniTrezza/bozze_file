# Copyright 2023 Raffaele Amalfitano

from odoo import http
from odoo.http import request


class CdsController(http.Controller):


    # *********************************** REGISTRA OFFERTA ***********************************
    @http.route('/api/v1/cds/registra-offerta', type='json', methods=['POST', 'OPTIONS'],
                auth='jwt_cds', cors='*', csrf=False, save_session=False)
    def create_product_record(self, **kw):
        """
        Product template record creation
        """
        if request.httprequest.method == 'POST' or request.httprequest.method == 'OPTIONS':
            json_data = request.get_json_data()
            # used to call the defined general methods
            cds_lib = request.env['cds.lib'].sudo()
            if json_data:
                if 'params' in json_data:
                    params = json_data['params']
                    if(
                        'dati_solver' in params and 'tipo_servizio' in params and
                        'nome' in params and 'descrizione' in params
                    ):

                        # *************** mandatory data management ***************
                        if not params['dati_solver']:
                            return cds_lib._missing_mandatory_data("Specificare nodo 'dati_solver'!")
                        if not params['tipo_servizio']:
                            return cds_lib._missing_mandatory_data("Specificare attributo 'tipo_servizio'!")
                        if not params['nome']:
                            return cds_lib._missing_mandatory_data("Specificare attributo 'nome'!")
                        if not params['descrizione']:
                            return cds_lib._missing_mandatory_data("Specificare attributo 'descrizione'!")

                        dati_solver = params['dati_solver']
                        tipo_servizio = params['tipo_servizio']
                        nome = params['nome']  # product name
                        descrizione = params['descrizione']  # product description


                        # check data inside 'dati_solver' node
                        if 'id_esterno_solver' in dati_solver and 'nome' in dati_solver:

                            # *************** mandatory data management ***************
                            if not dati_solver['id_esterno_solver']:
                                return cds_lib._missing_mandatory_data("Specificare attributo 'id_esterno_solver' in 'dati_solver'!")
                            if not dati_solver['nome']:
                                return cds_lib._missing_mandatory_data("Specificare attributo 'nome' in 'dati_solver'!")

                            id_esterno_solver = dati_solver['id_esterno_solver']
                            nome_solver = dati_solver['nome']

                            # search for existing solver
                            solver_obj = request.env['res.partner'].sudo().search([
                                ('ref', '=', id_esterno_solver),
                                ('is_solver', '=', True)
                            ], limit=1)
                            if not solver_obj:
                                solver_obj = solver_obj.create({
                                    'company_type': 'person',
                                    'is_solver': True,
                                    'name': nome_solver,
                                    'ref': id_esterno_solver,
                                    'street': dati_solver['indirizzo'] if 'indirizzo' in dati_solver else False,
                                    'city': dati_solver['citta'] if 'citta' in dati_solver else False,
                                    'zip': dati_solver['cap'] if 'cap' in dati_solver else False,
                                    'email': dati_solver['email'] if 'email' in dati_solver else False,
                                    'phone': dati_solver['telefono'] if 'telefono' in dati_solver else False,
                                    'website': dati_solver['url'] if 'url' in dati_solver else False
                                })

                                # for non existing solver, check for organization data
                                if 'id_esterno_organizzazione' in dati_solver and dati_solver['id_esterno_organizzazione']:
                                    id_esterno_organizzazione = dati_solver['id_esterno_organizzazione']
                                    company_obj = request.env['res.partner'].sudo().search([
                                        ('ref', '=', id_esterno_organizzazione)
                                    ], limit=1)
                                    if not company_obj:
                                        if 'nome_organizzazione' in dati_solver and dati_solver['nome_organizzazione']:
                                            nome_organizzazione = dati_solver['nome_organizzazione']
                                        else:
                                            nome_organizzazione = id_esterno_organizzazione
                                        company_obj = company_obj.create({
                                            'name': nome_organizzazione,
                                            'company_type': 'company'
                                            })
                                    # link solver to the organization
                                    solver_obj.parent_id = company_obj.id

                        # tipo_servizio managament
                        service_type_obj = request.env['cds.service.type'].sudo().search([('name', '=', tipo_servizio)], limit=1)
                        if not service_type_obj:
                            return cds_lib._not_found_data("Tipo servizio '{}' non presente a sistema".format(tipo_servizio))
                        
                        # aree_tecnologiche_prioritarie_m4 managament
                        aree_tecn_list = request.env['cds.technological.area'].sudo()
                        if 'aree_tecnologiche_prioritarie_m4' in params and params['aree_tecnologiche_prioritarie_m4']:
                            for area in params['aree_tecnologiche_prioritarie_m4']:
                                area = area.strip()
                                area_obj = aree_tecn_list.search([('name', '=', area)], limit=1)
                                if not area_obj:
                                    return cds_lib._not_found_data("Area tecnologica '{}' non presente a sistema".format(area))
                                aree_tecn_list |= area_obj

                        # ambiti_applicazione managament
                        ambiti_applicazione_list = request.env['cds.application.scope'].sudo()
                        if 'ambiti_applicazione' in params and params['ambiti_applicazione']:
                            for ambito in params['ambiti_applicazione']:
                                ambito = ambito.strip()
                                ambito_obj = ambiti_applicazione_list.search([('name', '=', ambito)], limit=1)
                                if not ambito_obj:
                                    return cds_lib._not_found_data("Ambito applicazione '{}' non presente a sistema".format(ambito))
                                ambiti_applicazione_list |= ambito_obj

                        # settori management
                        settori_list = request.env['cds.application.sector'].sudo()
                        if 'settori' in params and params['settori']:
                            for settore in params['settori']:
                                settore = settore.strip()
                                settore_obj = settori_list.search([('name', '=', settore)], limit=1)
                                if not settore_obj:
                                    return cds_lib._not_found_data("Settore '{}' non presente a sistema".format(settore))
                                settori_list |= settore_obj

                        # aree_di_specializzazione_ris3 management
                        area_di_specializzazione_list = request.env['cds.ris3.area'].sudo()
                        if 'aree_di_specializzazione_ris3' in params and params['aree_di_specializzazione_ris3']:
                            for area in params['aree_di_specializzazione_ris3']:
                                area = area.strip()
                                area_obj = area_di_specializzazione_list.search([('name', '=', area)], limit=1)
                                if not area_obj:
                                    return cds_lib._not_found_data("Area di specializzazione ris3 '{}' non presente a sistema".format(area))
                                area_di_specializzazione_list |= area_obj

                        # trl management
                        trl_list = request.env['cds.trl.data'].sudo()
                        if 'trl' in params and params['trl']:
                            for trl in params['trl']:
                                trl = trl.strip()
                                trl_obj = trl_list.search([('name', '=', trl)], limit=1)
                                if not trl_obj:
                                    return cds_lib._not_found_data("TRL '{}' non presente a sistema".format(trl))
                                trl_list |= trl_obj

                        # product template creation
                        product_templ_obj = request.env['product.template'].sudo().create({
                            'detailed_type': 'service',
                            'name': nome,
                            'description': descrizione,
                            'supplier_id': solver_obj.id,
                            'cds_service_benefits': params['benefici'] if 'benefici' in params else False,
                            'cds_service_type_id': service_type_obj.id,
                            'cds_technological_area_ids': [(6, 0, aree_tecn_list.ids)],
                            'cds_application_scope_ids': [(6, 0, ambiti_applicazione_list.ids)],
                            'cds_application_sector_ids': [(6, 0, settori_list.ids)],
                            'cds_ris3_area_ids': [(6, 0, area_di_specializzazione_list.ids)],
                            'cds_trl_data_ids': [(6, 0, trl_list.ids)]
                        })

                        return {
                            'success': True,
                            'status': 200,  # OK, risorsa creata
                            'message': "Offerta creata con successo",
                            'offerta': {
                                'nome': product_templ_obj.name,
                                'descrizione': product_templ_obj.description,
                                'solver': product_templ_obj.supplier_id.name,
                                'organizzazione': product_templ_obj.supplier_id.parent_id.name if product_templ_obj.supplier_id.parent_id else None,
                                'benefici': product_templ_obj.cds_service_benefits,
                                'tipo_servizio': product_templ_obj.cds_service_type_id.name,
                                'aree_tecnologiche_prioritarie_m4': product_templ_obj.cds_technological_area_ids.mapped(lambda x: x.name),
                                'ambiti_applicazione': product_templ_obj.cds_application_scope_ids.mapped(lambda x: x.name),
                                'settori': product_templ_obj.cds_application_sector_ids.mapped(lambda x: x.name),
                                'aree_di_specializzazione_ris3': product_templ_obj.cds_ris3_area_ids.mapped(lambda x: x.name),
                                'trl': product_templ_obj.cds_trl_data_ids.mapped(lambda x: x.name)
                            }
                        }
                    else:
                        return cds_lib._missing_mandatory_data()
                else:
                    return cds_lib._missing_mandatory_data()
            else:
                return cds_lib._missing_mandatory_data()


    # *********************************** REGISTRA FABBISOGNO ***********************************
    @http.route('/api/v1/cds/registra-fabbisogno', type='json', methods=['POST', 'OPTIONS'],
                auth='jwt_cds', cors='*', csrf=False, save_session=False)
    def create_crm_record(self, **kw):
        """
        Crm record creation
        """
        if request.httprequest.method == 'POST' or request.httprequest.method == 'OPTIONS':
            json_data = request.get_json_data()
            # used to call the defined general methods
            cds_lib = request.env['cds.lib'].sudo()
            if json_data:
                if 'params' in json_data:
                    params = json_data['params']
                    if(
                        'dati_seeker' in params and 'descrizione_richiesta' in params and
                        'percorso_transizione_da_seguire' in params and 'tipo_servizio' in params
                    ):

                        # *************** mandatory data management ***************
                        if not params['dati_seeker']:
                            return cds_lib._missing_mandatory_data("Specificare nodo 'dati_seeker'!")
                        if not params['descrizione_richiesta']:
                            return cds_lib._missing_mandatory_data("Specificare attributo 'descrizione_richiesta'!")
                        if not params['percorso_transizione_da_seguire']:
                            return cds_lib._missing_mandatory_data("Specificare attributo 'percorso_transizione_da_seguire'!")
                        if not params['tipo_servizio']:
                            return cds_lib._missing_mandatory_data("Specificare attributo 'tipo_servizio'!")

                        dati_seeker = params['dati_seeker']
                        descrizione_richiesta = params['descrizione_richiesta'] # crm record name
                        percorso_transizione_da_seguire = params['percorso_transizione_da_seguire']
                        tipo_servizio = params['tipo_servizio']


                        # check data inside 'dati_seeker' node
                        if 'id_esterno_seeker' in dati_seeker and 'nome' in dati_seeker and 'tipo_contatto':

                            # *************** mandatory data management ***************
                            if not dati_seeker['id_esterno_seeker']:
                                return cds_lib._missing_mandatory_data("Specificare attributo 'id_esterno_seeker' in 'dati_seeker'!")
                            if not dati_seeker['nome']:
                                return cds_lib._missing_mandatory_data("Specificare attributo 'nome' in 'dati_seeker'!")
                            if not dati_seeker['tipo_contatto'] or dati_seeker['tipo_contatto'] not in ['persona_fisica', 'company']:
                                return cds_lib._missing_mandatory_data(
                                    "Specificare attributo 'tipo_contatto' in 'dati_seeker'! Il valore può essere 'persona_fisica' oppure 'company'!")

                            id_esterno_seeker = dati_seeker['id_esterno_seeker']
                            nome_seeker = dati_seeker['nome']
                            tipo_contatto = dati_seeker['tipo_contatto']

                            # search for existing seeker
                            seeker_obj = request.env['res.partner'].sudo().search([
                                ('ref', '=', id_esterno_seeker),
                                ('is_seeker', '=', True)
                            ], limit=1)
                            if not seeker_obj:
                                seeker_obj = seeker_obj.create({
                                    'company_type': 'person' if tipo_contatto == 'persona_fisica' else 'company',
                                    'is_seeker': True,
                                    'name': nome_seeker,
                                    'ref': id_esterno_seeker,
                                    'street': dati_seeker['indirizzo'] if 'indirizzo' in dati_seeker else False,
                                    'city': dati_seeker['citta'] if 'citta' in dati_seeker else False,
                                    'zip': dati_seeker['cap'] if 'cap' in dati_seeker else False,
                                    'email': dati_seeker['email'] if 'email' in dati_seeker else False,
                                    'phone': dati_seeker['telefono'] if 'telefono' in dati_seeker else False,
                                    # 'website': dati_seeker['url'] if 'url' in dati_seeker else False
                                })

                                # for non existing seeker, check for organization data
                                if 'id_esterno_organizzazione' in dati_seeker and dati_seeker['id_esterno_organizzazione']:
                                    id_esterno_organizzazione = dati_seeker['id_esterno_organizzazione']
                                    company_obj = request.env['res.partner'].sudo().search([
                                        ('ref', '=', id_esterno_organizzazione)
                                    ], limit=1)
                                    if not company_obj:
                                        if 'nome_organizzazione' in dati_seeker and dati_seeker['nome_organizzazione']:
                                            nome_organizzazione = dati_seeker['nome_organizzazione']
                                        else:
                                            nome_organizzazione = id_esterno_organizzazione
                                        company_obj = company_obj.create({
                                            'name': nome_organizzazione,
                                            'company_type': 'company'
                                            })
                                    # link seeker to the organization
                                    seeker_obj.parent_id = company_obj.id

                        # percorso_transizione_da_seguire managament
                        transition_path_obj = request.env['cds.transition.path'].sudo().search([('name', '=', percorso_transizione_da_seguire)], limit=1)
                        if not transition_path_obj:
                            return cds_lib._not_found_data("Percorso transizione da seguire '{}' non presente a sistema".format(percorso_transizione_da_seguire))

                        # tipo_servizio managament
                        service_type_obj = request.env['cds.service.type'].sudo().search([('name', '=', tipo_servizio)], limit=1)
                        if not service_type_obj:
                            return cds_lib._not_found_data("Tipo servizio '{}' non presente a sistema".format(tipo_servizio))
                        
                        # aree_tecnologiche_prioritarie_m4 managament
                        aree_tecn_list = request.env['cds.technological.area'].sudo()
                        if 'aree_tecnologiche_prioritarie_m4' in params and params['aree_tecnologiche_prioritarie_m4']:
                            for area in params['aree_tecnologiche_prioritarie_m4']:
                                area = area.strip()
                                area_obj = aree_tecn_list.search([('name', '=', area)], limit=1)
                                if not area_obj:
                                    return cds_lib._not_found_data("Area tecnologica '{}' non presente a sistema".format(area))
                                aree_tecn_list |= area_obj

                        # ambiti_applicazione managament
                        ambiti_applicazione_list = request.env['cds.application.scope'].sudo()
                        if 'ambiti_applicazione' in params and params['ambiti_applicazione']:
                            for ambito in params['ambiti_applicazione']:
                                ambito = ambito.strip()
                                ambito_obj = ambiti_applicazione_list.search([('name', '=', ambito)], limit=1)
                                if not ambito_obj:
                                    return cds_lib._not_found_data("Ambito applicazione '{}' non presente a sistema".format(ambito))
                                ambiti_applicazione_list |= ambito_obj

                        # settori management
                        settori_list = request.env['cds.application.sector'].sudo()
                        if 'settori' in params and params['settori']:
                            for settore in params['settori']:
                                settore = settore.strip()
                                settore_obj = settori_list.search([('name', '=', settore)], limit=1)
                                if not settore_obj:
                                    return cds_lib._not_found_data("Settore '{}' non presente a sistema".format(settore))
                                settori_list |= settore_obj

                        # aree_di_specializzazione_ris3 management
                        area_di_specializzazione_list = request.env['cds.ris3.area'].sudo()
                        if 'aree_di_specializzazione_ris3' in params and params['aree_di_specializzazione_ris3']:
                            for area in params['aree_di_specializzazione_ris3']:
                                area = area.strip()
                                area_obj = area_di_specializzazione_list.search([('name', '=', area)], limit=1)
                                if not area_obj:
                                    return cds_lib._not_found_data("Area di specializzazione ris3 '{}' non presente a sistema".format(area))
                                area_di_specializzazione_list |= area_obj

                        # trl management
                        trl_list = request.env['cds.trl.data'].sudo()
                        if 'trl' in params and params['trl']:
                            for trl in params['trl']:
                                trl = trl.strip()
                                trl_obj = trl_list.search([('name', '=', trl)], limit=1)
                                if not trl_obj:
                                    return cds_lib._not_found_data("TRL '{}' non presente a sistema".format(trl))
                                trl_list |= trl_obj

                        # crm lead record creation
                        crm_lead_obj = request.env['crm.lead'].sudo().create({
                            'type': 'opportunity',
                            'name': descrizione_richiesta,
                            # 'partner_id': seeker_obj.id,
                            'cds_transition_path_id': transition_path_obj.id,
                            'cds_service_type_id': service_type_obj.id,
                            'cds_technological_area_ids': [(6, 0, aree_tecn_list.ids)],
                            'cds_application_scope_ids': [(6, 0, ambiti_applicazione_list.ids)],
                            'cds_application_sector_ids': [(6, 0, settori_list.ids)],
                            'cds_ris3_area_ids': [(6, 0, area_di_specializzazione_list.ids)],
                            'cds_trl_data_ids': [(6, 0, trl_list.ids)]
                        })
                        # set partner in order to avoid lead enrichment mail error error during lead creation
                        crm_lead_obj.partner_id = seeker_obj.id

                        # apply matching method
                        cds_lib.service_matching(crm_lead_obj, service_type_obj)

                        lista_servizi_matchati = []
                        for service in crm_lead_obj.product_matched_ids:
                            lista_servizi_matchati.append({
                                'servizio': service.name,
                                'solver': service.supplier_id.name
                                })

                        return {
                            'success': True,
                            'status': 200,  # OK, risorsa creata
                            'message': "Fabbisogno creato con successo",
                            'servizi_matchati': lista_servizi_matchati
                        }
                    else:
                        return cds_lib._missing_mandatory_data()
                else:
                    return cds_lib._missing_mandatory_data()
            else:
                return cds_lib._missing_mandatory_data()


    # *********************************** GET OFFERTE ***********************************
    @http.route('/api/v1/cds/offerte', type="json", methods=['GET'],
        auth='jwt_cds', cors='*', csrf=False, save_session=False)
    def get_offerte(self, **kw):
        """
        GET request: retrieve products with solver specified
        """
        if request.httprequest.method == 'GET' or request.httprequest.method == 'OPTIONS':
            json_data = request.get_json_data()
            # used to call the defined general methods
            cds_lib = request.env['cds.lib'].sudo()
            if json_data:
                if 'params' in json_data:
                    params = json_data['params']
                    product_ids = request.env['product.template'].search([('supplier_id', '!=', False)])
                    product_list = []
                    for record in product_ids:
                        vals = {
                            'nome': record.name,
                            'descrizione': record.description,
                            'solver': record.supplier_id.name,
                            'organizzazione': record.supplier_id.parent_id.name if record.supplier_id.parent_id else None,
                            'benefici': record.cds_service_benefits,
                            'tipo_servizio': record.cds_service_type_id.name,
                            'aree_tecnologiche_prioritarie_m4': record.cds_technological_area_ids.mapped(lambda x: x.name),
                            'ambiti_applicazione': record.cds_application_scope_ids.mapped(lambda x: x.name),
                            'settori': record.cds_application_sector_ids.mapped(lambda x: x.name),
                            'aree_di_specializzazione_ris3': record.cds_ris3_area_ids.mapped(lambda x: x.name),
                            'trl': record.cds_trl_data_ids.mapped(lambda x: x.name)
                        }
                        product_list.append(vals)
                    return {
                        'success': True,
                        'status': 200, # request OK
                        'message': "Elenco offerte restituite con successo",
                        'elenco_offerte': product_list,
                    }
                else:
                    return cds_lib._missing_mandatory_data()
            else:
                return cds_lib._missing_mandatory_data()


    # *********************************** GET FABBISOGNI ***********************************
    @http.route('/api/v1/cds/fabbisogni', type="json", methods=['GET'],
        auth='jwt_cds', cors='*', csrf=False, save_session=False)
    def get_fabbisogni(self, **kw):
        """
        GET request: retrieve crm records
        """
        if request.httprequest.method == 'GET' or request.httprequest.method == 'OPTIONS':
            json_data = request.get_json_data()
            # used to call the defined general methods
            cds_lib = request.env['cds.lib'].sudo()
            if json_data:
                if 'params' in json_data:
                    params = json_data['params']
                    crm_ids = request.env['crm.lead'].search([])
                    crm_list = []
                    for record in crm_ids:
                        lista_servizi_matchati = []
                        for service in record.product_matched_ids:
                            lista_servizi_matchati.append({
                                'servizio': service.name,
                                'solver': service.supplier_id.name
                                })
                        vals = {
                            'descrizione_richiesta': record.name,
                            'seeker': record.partner_id.name,
                            'organizzazione': record.partner_id.parent_id.name if record.partner_id.parent_id else None,
                            'percorso_transizione_da_seguire': record.cds_transition_path_id.name,
                            'tipo_servizio': record.cds_service_type_id.name,
                            'aree_tecnologiche_prioritarie_m4': record.cds_technological_area_ids.mapped(lambda x: x.name),
                            'ambiti_applicazione': record.cds_application_scope_ids.mapped(lambda x: x.name),
                            'settori': record.cds_application_sector_ids.mapped(lambda x: x.name),
                            'aree_di_specializzazione_ris3': record.cds_ris3_area_ids.mapped(lambda x: x.name),
                            'trl': record.cds_trl_data_ids.mapped(lambda x: x.name),
                            'servizi_matchati': lista_servizi_matchati
                        }
                        crm_list.append(vals)
                    return {
                        'success': True,
                        'status': 200, # request OK
                        'message': "Elenco fabbisogni restituiti con successo",
                        'elenco_fabbisogni': crm_list,
                    }
                else:
                    return cds_lib._missing_mandatory_data()
            else:
                return cds_lib._missing_mandatory_data()
