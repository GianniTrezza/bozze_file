# from odoo import http, fields
# from odoo.http import request, Response
# from odoo.tools.safe_eval import json
# import logging

# _logger = logging.getLogger(__name__)

# class MyController(http.Controller):

#     @http.route('/print_invoices', type='http', auth='public', csrf=False)
#     def print_invoices(self):
#         invoice_records = request.env['account.move'].sudo().search([])
#         for invoice in invoice_records:
#             print("ID FATTURA : ", invoice.id)
#             print("Referenza:", invoice.refer)
#             print("Stato:", invoice.state)
#         return "postate"
# class Fatture(http.Controller):
#     @http.route('/api/getfatture' , auth='public', csrf="*")
#     def get_fatture(self):
#         tutte_lefatture = http.request.env['accoun.move']
#         fatture = tutte_lefatture.sudo().search([])

# #https://odoo16-prenotazione-bb.unitivastaging.it/api/prova
# class RoomBookingController(http.Controller):
#     @http.route('/api/prova', cors='*', auth='public', methods=['POST'], csrf=False, website=False)
#     def handle_custom_endpoint(self, **post):
#         try:
#             json_data = request.httprequest.data
#             data_dict = json.loads(json_data)
#             _logger.info(f"Received data: {data_dict}")
            
#             if 'ping' in data_dict:
#                 _logger.info("Ping received")
#                 return Response("Pong", content_type='text/plain', status=200)
        
#             content = json.loads(data_dict.get("content"))
#         except json.JSONDecodeError as e:
#             _logger.error(f"JSON Decode Error: {e}")
#             return Response("Invalid JSON format", content_type='text/plain', status=400)
#         except Exception as e:
#             _logger.exception("An unexpected error occurred")
#             return Response("Internal Server Error", content_type='text/plain', status=500)
        
#         room_name = content.get('roomNameGuest')
#         refer_ = content.get("refer")
#         guestsList_ = content.get("guestsList")
#         roomGross_ = content.get("roomGross")
#         totalGuest_ = content.get("totalGuest")
#         numero_stanza_ = content.get("rooms")
#         # nome_stanza= content.get("roomName")
#         priceBreakdown = content.get("priceBreakdown")
#         prezzo_unitario_ = priceBreakdown[0].get("price")
#         # **info cliente**
#         guests = content.get("guests")
#         checkin_ = guests[0].get("checkin")
#         checkout_ = guests[0].get("checkout")
#         city_ = guests[0].get("city")
#         email_ = guests[0].get("email")
#         phone_ = guests[0].get("phone")
#         address_ = guests[0].get("address")

#         tipo = data_dict.get('type')

#         checkin_date = fields.Date.from_string(checkin_)
#         checkout_date = fields.Date.from_string(checkout_)
#         delta = checkout_date - checkin_date
#         n_notti = delta.days
#         quantity_soggiorno = totalGuest_ * n_notti
#         print("Il nome della stanza prenotata è:", room_name)
#         response_data = {
#             "refer": refer_,
#             "prezzo totale": roomGross_,
#             "ospiti": totalGuest_,
#             "checkin": checkin_,
#             "checkout": checkout_,
#             "nome stanza": room_name,
#             "numero stanza": numero_stanza_,
#             "numero notti": n_notti,
#             "quantity_soggiorno": quantity_soggiorno,
#             "prezzo unitario": prezzo_unitario_,
#             "city_utente": city_,
#             "email": email_,
#             "guestsList": guestsList_,
#             "telefono": phone_,
#             "indirizzo": address_,
#             "tipo": tipo
#         }
#         contact_bb = request.env['res.partner'].sudo().create({
#                 'company_type': 'person',
#                 'name': guestsList_,
#                 'street': address_,
#                 'city': city_,
#                 'email': email_,
#                 'phone': phone_
#             })
#         customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
#         account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 107
#         journal_id = customer_invoice_journal.id
#         # contact_id = contact_bb.id
#         # intero_contact = int(contact_id)
#         # print("ID CONTATTO CREATO : ", intero_contact)
#         room_booking_obj = []
#         product = request.env['product.product'].sudo().search([('name', '=', room_name)], limit=1)
#         if not product:
#             _logger.info(f"Prodotto non trovato per il nome: {room_name}. Creazione di un nuovo prodotto.")
#             product = request.env['product.product'].sudo().create({'name': room_name})
#             room_booking_obj.append(product)
#         # else:
#         #     room_booking_obj.append(product)

#         if tipo == 'RESERVATION_CREATED':
#             room_booking_obj = request.env['account.move'].sudo().create({
#                 'state': 'draft',
#                 'journal_id': journal_id,
#                 'refer': refer_,
#                 'move_type': 'out_invoice',
#                 'checkin': checkin_,
#                 'checkout': checkout_,
#                 'totalGuest': totalGuest_,
#                 'rooms': n_notti,
#                 'roomName':room_name,
#                 'roomGross': roomGross_,
#                 'partner_id': contact_bb
#             })

#             linee_fattura = []
#             linea_fattura_pernotto = {
#                 'move_id': room_booking_obj.id,
#                 'product_id': product.id,
#                 'name': f"Prenotazione {refer_} dal {checkin_} al {checkout_}",
#                 'quantity': n_notti,
#                 'price_unit': prezzo_unitario_,
#                 'account_id': account_id
#             }
#             linee_fattura.append(linea_fattura_pernotto)
#             linea_fattura_tassasoggiorno = {
#                 'move_id': room_booking_obj.id,
#                 'product_id': 2,
#                 'name': "Tassa di soggiorno",
#                 'quantity': quantity_soggiorno,
#                 'price_unit': 2,
#                 'account_id': account_id
#             }
#             linee_fattura.append(linea_fattura_tassasoggiorno)
#             for line in linee_fattura:
#                 request.env['account.move.line'].sudo().create(line)

#             room_booking_obj.with_context(default_type='out_invoice').write({'state': 'draft'})

#         elif tipo == 'RESERVATION_CHANGE':

#             existing_invoice = request.env['account.move'].sudo().search([
#                 ('refer', '=', refer_),
#                 ('move_type', '=', 'out_invoice')
#             ], limit=1)

#             if existing_invoice:
#                 existing_invoice.write({
#                     'state': 'draft',
#                     'journal_id': journal_id,
#                     'refer': refer_,
#                     'move_type': 'out_invoice',
#                     'checkin': checkin_,
#                     'checkout': checkout_,
#                     'totalGuest': totalGuest_,
#                     'roomGross': roomGross_,
#                     'roomName':room_name,
#                 })
#                 existing_invoice_line_ids = existing_invoice.invoice_line_ids
#                 # Modifica le linee di fattura esistenti
#                 for line in existing_invoice_line_ids:
#                     if line.product_id.id == room_name:
#                         line.write({
#                             'name': f"Prenotazione {refer_} dal {checkin_} al {checkout_}",
#                             'quantity': n_notti,
#                             'price_unit': prezzo_unitario_
#                         })
#                     elif line.product_id.id == 2:
#                         line.write({
#                             'name': "Tassa di soggiorno",
#                             'quantity': quantity_soggiorno
#                         })
#             room_booking_obj = existing_invoice

#         elif tipo == 'RESERVATION_CANCELLED':

#             existing_invoice = request.env['account.move'].sudo().search([
#                 ('refer', '=', refer_),
#                 ('move_type', '=', 'out_invoice')
#             ], limit=1)

#             if existing_invoice:
#                 existing_invoice.write({
#                     'state': 'cancel'
#                 })
#                 room_booking_obj = existing_invoice
#         print("La fattura ha il seguente id ---------->", room_booking_obj.id)
#         print("Il prodotto ha il seguente id ---------->", product.id)
#         #room_booking_obj.action_post()
#         print("postata")
#         return Response(json.dumps(response_data), content_type='application/json')
#*****************************************prova*****************

#link https://odoo16-prenotazione-bb.unitivastaging.it/api/test

#*********************route****************************

# class AccountController(http.Controller):
#     @http.route('/api/get_accounts', auth='public', csrf=False)
#     def get_accounts(self):
#         account_model = http.request.env['account.account']
#         accounts = account_model.sudo().search([])
#
#         account_list = []
#         for account in accounts:
#             account_info = {
#                 'id': account.id,
#                 'name': account.name,
#                 'code': account.code,
#             }
#             account_list.append(account_info)
#
#         return account_list
# import json

# def extract_room_name(json_data):
#     try:
#         # Load the JSON data as a dictionary
#         data = json.loads(json_data)
        
#         # Extract the roomName
#         room_name = data.get('roomName', None)
        
#         # Now, room_name can be used to map to the product_id in your system
#         return room_name
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")
#         return None

# # Your JSON content string
# json_content = '{"cancelPenality":-1,"cityTaxZero":false,"extraIncluded":[],"json":{},"loyaltyDiscount":false,"refer":"XB0GL1","channelId":288,"channelRefer":"XB0GL1","status":"CONFIRMED","checkin":"2023-11-03T11:00:00Z[UTC]","checkout":"2023-11-03T23:00:00Z[UTC]","createTime":"2023-11-03T10:12:27Z[UTC]","updateTime":"2023-11-03T10:12:27Z[UTC]","children":0,"guests":[{"checkin":"2023-11-03","checkout":"2023-11-04","city":"","email":"Phoebe@octorate.com","familyName":"Buffay","givenName":"Phoebe","language":"EN","phone":"","source":"USER","type":"BOOKER"}],"infants":0,"phone":"","roomGross":500.00,"totalGross":500.00,"totalGuest":2,"accommodation":{"address":"via filippo caruso","checkinEnd":20,"checkinStart":12,"checkout":12,"city":"ROMA","currency":"EUR","id":"557782","latitude":41.8489657,"longitude":12.5764685,"name":"OdooERP Test Api Building L.A.","phoneNumber":"+3906060606","timeZone":"Europe/Rome","timeZoneOffset":"+01:00","zipCode":"00173"},"arrivalTime":"12:00:00","autoLoginParam":"5597d8414c504ed138b68bb62662ad3872180b7d47c44d280bcf67bbf21a7a14e9f10122c00541ad391cc38e1135f39b","channelName":"octoevo autosubmit","currency":"EUR","firstName":"Phoebe","freeCancellation":true,"grouped":false,"guestMailAddress":"Phoebe@octorate.com","guestsList":"Phoebe Buffay","id":105099844,"itemCompleted":false,"lastName":"Buffay","noShow":false,"paymentStatus":"UNPAID","paymentType":"UNKNOWN","payments":[],"priceBreakdown":[{"type":"DAILY_ROOM_PRICE","name":null,"createTime":null,"day":"2023-11-02T23:00:00Z[UTC]","price":500.00,"reference":"64857694","externalId":null,"included":true,"product":null,"quantity":null},{"type":"ROOM_NET","name":null,"createTime":null,"day":null,"price":500.00,"reference":null,"externalId":null,"included":true,"product":null,"quantity":null},{"type":"VAT","name":null,"createTime":null,"day":null,"price":0.00,"reference":null,"externalId":null,"included":true,"product":null,"quantity":null}],"product":599456,"roomName":"Building Los Angeles Apartment 101","roomNameGuest":"Building Los Angeles Apartment 101","rooms":1,"totalChildren":0,"totalInfants":0,"totalPaid":0.00,"touristTax":0}'

# # Use the function to get the roomName
# room_name = extract_room_name(json_content)

# print(f"The extracted roomName is: {room_name}")

# This is where you'd map the room_name to a product_id, for example:
# product_id = product_mapping.get(room_name)









     # ***** TASSA SOGIORNO ******
# delta = checkout - check in
# n_notti = delta.days
#quantity = numero_ospiti*delta

    # ***** PERNOTTO *******



#name = f"Prenotazione {invoice.refer} dal {checkin} al {checkout}"
#quantity = numero stanze

        # room_booking_obj = request.env['account.move']
        # new_invoice = room_booking_obj.sudo().create({
        #     'refer': refer,
        #     'checkin': checkin,
        #     'checkout': checkout,
        #     'totalGuest': totalGuest,
        #     'roomGross': roomGross,
        #     'partner_id': 36
        #     # Altri campi del tuo modello che devono essere impostati
        # })

#********************************************************************************************************
# else:
#     print("fallito")
# from odoo import http
# from odoo.http import request
# import json
#
# class ThirdPartyConnector(http.Controller):
#     @http.route('/third_party_connector/receive_data', type='json', auth='user', methods=['POST'], csrf=False)
#     def receive_data(self, **kwargs):
#         data = request.jsonrequest
#
#         if data:
#             try:
#                 model = "account.move"
#                 type = data.get('type')
#
#                 # Estrazione dati dal JSON
#                 content_data = json.loads(data.get('content')) if data.get('content') else {}
#
#                 # Fiedls di interesse
#                 fields = {
#                     'refer': content_data.get('refer'),
#                     'checkin': content_data.get('checkin').split('T')[0] if content_data.get('checkin') else False,
#                     'checkout': content_data.get('checkout').split('T')[0] if content_data.get('checkout') else False,
#                     'totalGuest': content_data.get('totalGuest'),
#                     'totalChildren': content_data.get('children'),
#                     'totalInfants': content_data.get('infants'),
#                     'rooms': content_data.get('rooms'),
#                     'roomGross': content_data.get('roomGross'),
#                     # altri fields possono essere aggiunti qui in base alle necessità
#                 }
#
#                 if type == 'RESERVATION_CREATED':
#
#                     fields['state'] = 'draft'
#                     record = request.env[model].create(fields)
#                     return {'success': True, 'record_id': record.id}
#
#                 elif type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
#                     # cerca il record esistente tramite ID di riferimento, aggiorna lo stato e lascia invariati gli altri campi
#                     refer_id = fields.get('refer')
#                     record = request.env[model].search([('refer', '=', refer_id)])
#
#
#
#                 else:
#                     return {'error': 'Invalid type'}
#
#             except Exception as e:
#                 return {'error': str(e)}
#
#         return {'error': 'Invalid data'}

# **************************************************CODICE ORIGINALE******************************************************************
# class ResPartner(models.Model):
#     _inherit = 'res.partner'

#     def name_get(self):
#         result = []
#         for partner in self:
#             name = partner.name
#             if partner.email:
#                 name = f"{name} - {partner.email}"

#             result.append((partner.id, name))
#         return result

from odoo import http, models
from odoo import _
from odoo.http import request, Response
import json
import datetime
import logging


_logger = logging.getLogger(__name__)

class RoomBookingController(http.Controller):

    @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
    def handle_custom_endpoint(self, **post):
        json_data = request.httprequest.data
        data_dict = json.loads(json_data)
        content = json.loads(data_dict.get("content"))
        create_time_str = data_dict.get("createTime")

        try:
            create_time = datetime.datetime.strptime(create_time_str, '%Y-%m-%dT%H:%M:%SZ[UTC]') if create_time_str else None
        except ValueError:
            return Response("Invalid date format for createTime", content_type='text/plain', status=400)

        if not content.get("refer") or not content.get("guests"):
            return Response("Missing required fields", content_type='text/plain', status=400)

        checkin_str = content.get("guests")[0].get("checkin")
        checkout_str = content.get("guests")[0].get("checkout")
        
        try:
            checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
            checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
        except ValueError:
            return Response("Invalid date format", content_type='text/plain', status=400)

        reservation_data = {
            'partner_id': content.get("guestsList"),
            'email': content.get("guestMailAddress"),
            'refer': content.get("refer"),
            # 'ref': content.get('roomNameGuest'),
            'ref': content.get('pmsProduct'),
            # potrebbe essere pmsProduct
            'roomName': content.get('roomName'),
            'checkin': checkin_date,
            'checkout': checkout_date,
            'channelNotes': content.get("channelNotes"),
            'totalGuest': content.get("totalGuest"),
            'totalChildren': content.get("totalChildren"),
            'totalInfants': content.get("totalInfants"),
            'rooms': content.get("rooms"),
            'roomGross': content.get("roomGross"),
            'invoicedate': create_time,
            # 'sistemazione': content.get("accommodation"),
        }
        
        event_type = data_dict.get("type")
        response_data = {}

        if event_type == "RESERVATION_CREATED":
            invoice_details = self.calculate_invoice_details(reservation_data)
            self.create_invoice(reservation_data, invoice_details)
            response_data.update(invoice_details)
        elif event_type == "RESERVATION_CHANGE":
            refer_id = reservation_data.get('refer')
            nome_cliente=reservation_data.get('partner_id')

            invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id), ('partner_id', '=', nome_cliente)], limit=1)
            if not invoice_record:
                return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
            # reservation_data.pop('partner_id', None)
            reservation_data.pop('email', None)
            if 'email' in request.env['account.move']._fields:
                invoice_record.sudo().write({'email': content.get("guestMailAddress")})

            # invoice_record.sudo().write(reservation_data)
        
            self.update_invoice_lines(invoice_record, reservation_data)
            response_data.update({
                # "Nome Ospite": reservation_data['partner_id'],
                # "partner_id": invoice_record.partner_id.name,
                "partner_id": invoice_record.partner_id.name,
                "move_id": invoice_record.id,
                "checkin": invoice_record.checkin.strftime('%Y-%m-%d') if isinstance(invoice_record.checkin, datetime.date) else invoice_record.checkin,
                "checkout": invoice_record.checkout.strftime('%Y-%m-%d') if isinstance(invoice_record.checkout, datetime.date) else invoice_record.checkout,
                "invoice_date": invoice_record.invoice_date.strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(invoice_record.invoice_date, datetime.datetime) else invoice_record.invoice_date,
                "totalGuest": invoice_record.totalGuest,
                "totalChildren": invoice_record.totalChildren,
                "totalInfants": invoice_record.totalInfants,
                "rooms": invoice_record.rooms,
                "product_id": invoice_record.roomName,
                "note aggiuntive": invoice_record.channelNotes,
                # "ref":invoice_record.roomNameGuest,
                "ref":invoice_record.pmsProduct,
                # "roomGross": invoice_record.roomGross,
                "state": invoice_record.state, 
            })
        elif event_type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
            refer_id = reservation_data.get('refer')
            checkout_id=reservation_data.get('checkout')
            
            # Search for the invoice by its reference
            invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
            if not invoice_record:
                return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)

            if invoice_record.checkout != checkout_id:
                return Response(f"Invoice found with refer: {refer_id}, but with different checkout date.", content_type='text/plain', status=400)

            new_state = 'cancel' if event_type == 'RESERVATION_CANCELLED' else 'posted'
            invoice_record.sudo().write({'state': new_state})
        # Converti tutti gli oggetti datetime in stringhe prima di serializzare in JSON
        else:
            return Response("Invalid event type", content_type='text/plain', status=400)
        
        # for key, value in response_data.items():
        #     if isinstance(value, datetime.datetime):
        #         response_data[key] = value.strftime('%Y-%m-%dT%H:%M:%SZ')
        # return Response(json.dumps(response_data), content_type='application/json', status=200)
        for key, value in response_data.items():
            if isinstance(value, datetime.date):
                response_data[key] = value.strftime('%Y-%m-%d')

        return Response(json.dumps(response_data), content_type='application/json', status=200)

    def calculate_invoice_details(self, reservation_data):
        nome_ospite= reservation_data['partner_id']
        checkin_date = reservation_data['checkin']
        
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        num_ospiti = reservation_data['totalGuest']

        tourist_tax_quantity = num_notti * num_ospiti * 2
        
        booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
        booking_quantity = reservation_data['rooms']
        booking_price_unit = reservation_data['roomGross']
        nome_stanza = reservation_data['roomName']
    
        return {
            "Orario creazione prenotazione": reservation_data["invoicedate"].strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(reservation_data["invoicedate"], datetime.datetime) else reservation_data["invoicedate"],
            "Nome ospite": nome_ospite,
            "Valore tassa turistica": tourist_tax_quantity,
            "Identificativo della prenotazione": booking_name,
            "Numero stanze": booking_quantity,
            "Costo stanza": booking_price_unit,
            "Tipologia stanza": nome_stanza,
            "Numero identificativo Camera": reservation_data["ref"]
            
        }
    def create_invoice(self, reservation_data, invoice_details):
        tax_0_percent = None
        partner_name = reservation_data['partner_id']
        nome_stanza = reservation_data['roomName']
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        # room_name = reservation_data['roomNameGuest']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        

        
        

        # partner = request.env['res.partner'].sudo().search([('name', '=', partner_name)], limit=1)
        partner = request.env['res.partner'].sudo().with_context(partner_display='invoice_partner_display_name').search([('name', '=', partner_name)], limit=1)

        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': partner_name,
                'email': reservation_data.get('email'),
                'customer_rank': 1
            })
            # Vecchio codice
            # partner = request.env['res.partner'].sudo().create({'name': partner_name, 'customer_rank': 1})
        # INIZIO RETTIFICA
        # pernotto_product = request.env['product.product'].sudo().search([('name', '=', 'Pernotto')], limit=1)
        # if not pernotto_product:
        #     pernotto_product = request.env['product.product'].sudo().create({
        #         'name': 'Pernotto',
        #         'type': 'service',
        #     })
        # room_product = request.env['product.product'].sudo().search([('name', '=', nome_stanza)], limit=1)
        room_product = request.env['product.product'].sudo().search([('name', '=', nome_stanza)])
        if not room_product:
            room_product = request.env['product.product'].sudo().create({'name': nome_stanza})
            # Handle the case where the product does not exist, perhaps create it or raise an error
        # else:
        #     raise ValueError(f"No product found with name: {nome_stanza}")
        

        tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
        if not tassa_soggiorno_product:
            tax_0_percent = request.env['account.tax'].sudo().search(
                [('amount_type', '=', 'percent'), ('type_tax_use', '=', 'sale'), ('amount', '=', 0)],
                limit=1
            )
            if not tax_0_percent:
                raise ValueError("Non esiste un'imposta al 0% nel sistema. Creala o assegnala manualmente.")
            
            vals = {
                'name': 'Tassa di Soggiorno',
                'type': 'service',
            }
            
            if tax_0_percent is not None:
                vals['taxes_id'] = [(6, 0, [tax_0_percent.id])]

            tassa_soggiorno_product = request.env['product.product'].sudo().create(vals)
        # FINE RETTIFICA
        customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 44
        journal_id = customer_invoice_journal.id
        try:
            # contact_bb = request.env['res.partner'].sudo().create({
            #         'company_type': 'person',
            #         'name': reservation_data["partner_id"],
            #         'email': reservation_data["email"],
            #         })
            partner_values = {
                'name': reservation_data["partner_id"],
                'email': reservation_data["email"],
                # 'indirizzo cliente': reservation_data["indirizzo"],
            }
            # print(f"La sistemazione ha le seguenti features:", reservation_data["sistemazione"])
            print(f"Il cliente presenta le seguenti features:", partner_values)
            partner = request.env['res.partner'].sudo().create(partner_values)
            print(f"Il cliente presenta il seguente ID:", partner)
            _logger.debug("Partner ID: %s", partner.id)

            partner_display_name = partner.name_get()[0][1] if partner else "Nuovo Partner"
            
            invoice_values = {
                'journal_id': journal_id,
                'move_type': 'out_invoice',
                'ref': reservation_data['ref'],
                # 'roomNameGuest': reservation_data['roomNameGuest'],
                'partner_id': partner.id,
                'invoice_partner_display_name': partner_display_name,
                'checkin': reservation_data['checkin'],
                'checkout': reservation_data['checkout'],
                'refer': reservation_data['refer'],
                'totalGuest': reservation_data['totalGuest'],
                'totalChildren': reservation_data['totalChildren'],
                'rooms': reservation_data['rooms'],
                'roomGross': reservation_data['roomGross'],
                'invoice_date': reservation_data['invoicedate'],
                'channelNotes': reservation_data['channelNotes'],
            }
            invoice_record = request.env['account.move'].sudo().create(invoice_values)
            invoice_record.message_post(
                body=f"<p><b><font size='4' face='Arial'>Dati di fatturazione creati:</font></b><br>"
                    f"Nome Cliente: {reservation_data['partner_id']}<br>"
                    f"Refer: {reservation_data['refer']}<br>"
                    f"Data Fattura: {reservation_data['invoicedate']}<br>"
                    f"Checkin: {checkin_date}<br>"
                    f"Checkout: {checkout_date}<br>"
                    f"Nome stanza: {nome_stanza}<br></p>"
                    f"Note stanza aggiuntive: {reservation_data['channelNotes']}<br>"
                    f"Numero bambini: {reservation_data['totalChildren']}<br>"
                    f"Ospiti: {reservation_data['totalGuest']}<br>"
                    f"Prezzo totale: {reservation_data['roomGross']}<br>",
                message_type='comment'
            )
        #     reservation_data = {
        #     'partner_id': content.get("guestsList"),
        #     'email': content.get("guestMailAddress"),
        #     'refer': content.get("refer"),
        #     # 'ref': content.get('roomNameGuest'),
        #     'ref': content.get('pmsProduct'),
        #     # potrebbe essere pmsProduct
        #     'roomName': content.get('roomName'),
        #     'checkin': checkin_date,
        #     'checkout': checkout_date,
        #     'totalGuest': content.get("totalGuest"),
        #     'totalChildren': content.get("totalChildren"),
        #     'totalInfants': content.get("totalInfants"),
        #     'rooms': content.get("rooms"),
        #     'roomGross': content.get("roomGross"),
        #     'invoicedate': create_time,
        #     # 'sistemazione': content.get("accommodation"),
        # }
        except Exception as e:
            _logger.error("Impossibile creare la fattura: %s", str(e))
            return Response("Errore interno del server", content_type='text/plain', status=500)

        # checkin_date = reservation_data['checkin']
        # checkout_date = reservation_data['checkout']
        # delta = checkout_date - checkin_date
        # num_notti = delta.days
        # num_ospiti = reservation_data['totalGuest']

        # tourist_tax_quantity = num_notti * num_ospiti * 2
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days


        booking_line_values = {
            'move_id': invoice_record.id,
            'product_id': room_product.id,
            'name': invoice_details['Identificativo della prenotazione'],
            'quantity': reservation_data['rooms'],
            'price_unit': invoice_details['Costo stanza'],
            # 'price_subtotal':tourist_tax_quantity,
            'account_id': account_id
        }
        request.env['account.move.line'].sudo().create(booking_line_values)

        # Create tourist tax line
        tourist_tax_line_values = {
            'move_id': invoice_record.id,
            'product_id': tassa_soggiorno_product.id,
            'name': "Tassa soggiorno",
            'quantity': reservation_data['totalGuest']*num_notti,
            'price_unit': 2,
            'account_id': account_id
            # 'account_id': 44  # Assumed account ID, you should replace with the actual account id for this transaction type
        }
        
        request.env['account.move.line'].sudo().create(tourist_tax_line_values)
    def update_invoice_lines(self, invoice_record, reservation_data):
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        # room_name = reservation_data['roomNameGuest']
        total_guest = reservation_data['totalGuest']
        total_children = reservation_data['totalChildren']
        rooms = reservation_data['rooms']
        room_gross= reservation_data['roomGross']
        room_name_guest= reservation_data['ref']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        formatted_invoice_date = reservation_data['invoicedate'].strftime('%Y-%m-%d') if isinstance(reservation_data['invoicedate'], datetime.datetime) else reservation_data['invoicedate']
        


        update_values = {
            'invoice_date': formatted_invoice_date,
            'checkin': checkin_date,
            'checkout': checkout_date, 
            'totalGuest': total_guest,
            'totalChildren':total_children,
            'rooms': rooms,
            'roomGross': room_gross, 
            'ref': room_name_guest,
            'channelNotes': reservation_data['channelNotes']
        }
        
        invoice_record.sudo().write(update_values)
        invoice_record.message_post(
                body=f"<p><b><font size='4' face='Arial'>Dati aggiornati:</font></b><br>"
                    f"Nome Cliente: {reservation_data['partner_id']}<br>"
                    f"Refer: {reservation_data['refer']}<br>"
                    f"Data Fattura: {reservation_data['invoicedate']}<br>"
                    f"Checkin: {checkin_date}<br>"
                    f"Checkout: {checkout_date}<br>"
                    f"Nome stanza: {reservation_data['roomName']}<br></p>"
                    f"Note stanza aggiuntive: {reservation_data['channelNotes']}<br>"
                    f"Numero bambini: {reservation_data['totalChildren']}<br>"
                    f"Ospiti: {reservation_data['totalGuest']}<br>"
                    f"Prezzo totale: {reservation_data['roomGross']}<br>",
                message_type='comment'
            )
        booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
        # invoice_record.write({'invoice_date': reservation_data['invoicedate'].strftime('%Y-%m-%d') if isinstance(reservation_data['invoicedate'], datetime.date) else reservation_data['invoicedate']})
        for line in invoice_record.invoice_line_ids:
            if line.product_id.name == reservation_data['roomName']:
                line.write({'name': booking_name})
                line.write({'price_unit': reservation_data['roomGross']})
                line.write({'quantity': reservation_data['rooms']})
            elif line.product_id.name == 'Tassa di Soggiorno':
                line.write({'quantity': reservation_data['totalGuest'] * num_notti})
                line.write({'price_unit': 2})
                pass
