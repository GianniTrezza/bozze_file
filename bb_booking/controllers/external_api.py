# from odoo import http
# from odoo.http import request, Response
# from odoo.tools.safe_eval import json
# from werkzeug.wrappers import Response
# import datetime
# import jwt
# import os
# import secrets

# # I tuoi segreti e credenziali
# # secret = os.urandom(24).hex()
# # print(f"Secret Key: {secret}")
# # algorithm = 'HS256'

# secret_key = secrets.token_hex(32)
# print(secret_key)

# algorithm = 'HS256'


# audience = 'auth_jwt_odoo_octorate' 
# issuer = 'third_party_connector issuer'

# payload = {
#     'some': 'payload',  # inserisci qui i tuoi dati di payload
#     'exp': datetime.datetime(year=9999, month=12, day=31), 
#     'aud': 'auth_jwt_odoo_octorate',
#     'iss': 'third_party_connector issuer'
# }

# encoded_jwt = jwt.encode(payload, secret_key, algorithm=algorithm)

# print(f"il token di accesso jwt è", encoded_jwt)



# # Parametri per il token JWT
# payload = {
#     'some': 'payload',
#     # 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60), # 60 secondi di validità
#     'aud': 'your_audience',
#     'iss': 'your_issuer'
# }
# secret = 'your_secret_key'
# algorithm = 'HS256'  # o qualsiasi altro algoritmo che usi, come 'RS256'

# # Genera il token
# encoded_jwt = jwt.encode(payload, secret, algorithm=algorithm)

# print(encoded_jwt)

#**************************************QUESTO CODICE FUNZIONA NELLA GENERAZIONE DELLE SINGOLE PRENOTAZIONI IN POSTMAN*****************



#https://odoo16-prenotazione-bb.unitivastaging.it/api/test


#*********************route****************************
# class RoomBookingController(http.Controller):
#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         try:
#             data_dict = json.loads(json_data)
#             content = json.loads(data_dict.get("content"))

#         except ValueError:
#             return "Errore nella formattazione dei dati JSON"

#             # Estrai il valore del campo 'checkin' dal dizionario dei dati
#         refer = content.get("refer")
#         # roomGross = content.get("roomGross")
#         totalGuest = content.get("totalGuest")
#         guests = content.get("guests")
#         checkin = guests[0].get("checkin")
#         checkout = guests[0].get("checkout")
#         totalChildren = content.get("totalChildren")  # Aggiungi queste righe per altri dati che vuoi estrarre
#         totalInfants = content.get("totalInfants")
#         rooms = content.get("rooms")
#         roomGross = content.get("roomGross")
#         reservation_data = {
#                 'refer': refer,
#                 'checkin': checkin,
#                 'checkout': checkout,
#                 'totalGuest': totalGuest,
#                 'totalChildren': totalChildren,
#                 'totalInfants': totalInfants,
#                 'rooms': rooms,
#                 'roomGross': roomGross
#             }


#         # reservation_data = {
#         #     "refer": refer,
#         #     # "prezzo": roomGross,
#         #     "totalGuest" : totalGuest,
#         #     "checkin" : checkin,
#         #     "checkout": checkout

#         # }
#         try:
#             new_move = request.env['account.move'].sudo().create(reservation_data)
#         except Exception as e:
#             return str(e)

#         # Creare un dizionario con i dati che desideri restituire
#         response_data = {
#             "move_id": new_move.id,
#             "refer": new_move.refer,
#             "checkin": new_move.checkin.strftime('%Y-%m-%d') if isinstance(new_move.checkin, datetime.date) else new_move.checkin,
#             "checkout": new_move.checkout.strftime('%Y-%m-%d') if isinstance(new_move.checkout, datetime.date) else new_move.checkout,
#             "totalGuest": new_move.totalGuest,
#             "totalChildren": new_move.totalChildren,
#             "totalInfants": new_move.totalInfants,
#             "rooms": new_move.rooms,
#             "roomGross": new_move.roomGross,
#         }

#         # Convertire il dizionario in JSON e restituirlo
#         return Response(json.dumps(response_data), content_type='application/json')

#*****************************************CONSIDERAZIONE DEGLI EVENTS*****************
# from odoo import http
# from odoo.http import request, Response
# from odoo.tools.safe_eval import json
# import datetime

# class RoomBookingController(http.Controller):
#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         try:
#             data_dict = json.loads(json_data)
#             content = json.loads(data_dict.get("content"))
#             type = data_dict.get("type")
#         except ValueError:
#             return Response("Errore nella formattazione dei dati JSON", content_type='text/plain', status=400)

#         reservation_data = {
#             'refer': content.get("refer"),
#             'checkin': content.get("guests")[0].get("checkin"),
#             'checkout': content.get("guests")[0].get("checkout"),
#             'totalGuest': content.get("totalGuest"),
#             'totalChildren': content.get("totalChildren"),
#             'totalInfants': content.get("totalInfants"),
#             'rooms': content.get("rooms"),
#             'roomGross': content.get("roomGross")
#         }

#         try:
#             model = 'account.move' 

#             if type == 'RESERVATION_CREATED':
#                 reservation_data['state'] = 'draft'
#                 new_move = request.env[model].sudo().create(reservation_data)
#                 response_data = {
#                     "move_id": new_move.id,
#                     "refer": new_move.refer,
#                     "checkin": new_move.checkin.strftime('%Y-%m-%d') if isinstance(new_move.checkin, datetime.date) else new_move.checkin,
#                     "checkout": new_move.checkout.strftime('%Y-%m-%d') if isinstance(new_move.checkout, datetime.date) else new_move.checkout,
#                     "totalGuest": new_move.totalGuest,
#                     "totalChildren": new_move.totalChildren,
#                     "totalInfants": new_move.totalInfants,
#                     "rooms": new_move.rooms,
#                     "roomGross": new_move.roomGross,
#                     "state": new_move.state,
#                 }

#             elif type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
#                 refer_id = reservation_data.get('refer')
#                 # record = request.env[model].sudo().search([('refer', '=', refer_id)])
#                 record = request.env[model].sudo().search([('refer', '=', refer_id)], limit=1)

#                 if not record:
#                     return Response("No reservation found with the provided refer ID", content_type='text/plain', status=400)
                
#                 # new_state = 'cancelled' if type == 'RESERVATION_CANCELLED' else 'confirmed'
#                 new_state = 'cancel' if type == 'RESERVATION_CANCELLED' else 'posted'
#                 record.sudo().write({'state': new_state})
#                 response_data = {
#                     "move_id": record.id,
#                     "refer": record.refer,
#                     "checkin": record.checkin.strftime('%Y-%m-%d') if isinstance(record.checkin, datetime.date) else record.checkin,
#                     "checkout": record.checkout.strftime('%Y-%m-%d') if isinstance(record.checkout, datetime.date) else record.checkout,
#                     "totalGuest": record.totalGuest,
#                     "totalChildren": record.totalChildren,
#                     "totalInfants": record.totalInfants,
#                     "rooms": record.rooms,
#                     "roomGross": record.roomGross,
#                     "state": record.state, 
#                 }

#             else:
#                 return Response("Invalid type", content_type='text/plain', status=400)

#         except Exception as e:
#             return Response(str(e), content_type='text/plain', status=500)

#         return Response(json.dumps(response_data), content_type='application/json')

# FINE CODICE VALIDO

#*************************************NEW CODE: GENERAZIONE FATTURA ODOO *********************
# from odoo import http
# from odoo.http import request, Response
# import json
# import datetime

# class RoomBookingController(http.Controller):
#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         data_dict = json.loads(json_data)
#         content = json.loads(data_dict.get("content"))
#         type = data_dict.get("type")

#         # Validazione dei dati in entrata
#         if not content.get("refer") or not content.get("guests"):
#             return Response("Missing required fields", content_type='text/plain', status=400)

#         checkin_str = content.get("guests")[0].get("checkin")
#         checkout_str = content.get("guests")[0].get("checkout")

#         # Convalida e conversione delle date
#         try:
#             checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
#             checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
#         except ValueError:
#             return Response("Invalid date format", content_type='text/plain', status=400)

#         reservation_data = {
#             'refer': content.get("refer"),
#             'checkin': checkin_date,
#             'checkout': checkout_date,
#             'totalGuest': content.get("totalGuest"),
#             'totalChildren': content.get("totalChildren"),
#             'totalInfants': content.get("totalInfants"),
#             'rooms': content.get("rooms"),
#             'roomGross': content.get("roomGross")
#         }

#         model = 'account.move' 

#         if type == 'RESERVATION_CREATED':
#             partner = request.env['res.partner'].sudo().search([('name', '=', content.get("partner_name"))], limit=1)
#             if partner:
#                 reservation_data['partner_id'] = partner.id
#             new_move = request.env[model].sudo().create(reservation_data)
#             response_data = {
#                 "move_id": new_move.id,
#                 "refer": new_move.refer,
#                 "checkin": new_move.checkin.strftime('%Y-%m-%d') if isinstance(new_move.checkin, datetime.date) else new_move.checkin,
#                 "checkout": new_move.checkout.strftime('%Y-%m-%d') if isinstance(new_move.checkout, datetime.date) else new_move.checkout,
#                 "totalGuest": new_move.totalGuest,
#                 "totalChildren": new_move.totalChildren,
#                 "totalInfants": new_move.totalInfants,
#                 "rooms": new_move.rooms,
#                 "roomGross": new_move.roomGross,
#                 "state": new_move.state,
#             }

#         elif type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
#             refer_id = reservation_data.get('refer')
#             record = request.env[model].sudo().search([('refer', '=', refer_id)], limit=1)
#             new_state = 'cancel' if type == 'RESERVATION_CANCELLED' else 'posted'
#             record.sudo().write({'state': new_state})
#             response_data = {
#                 "move_id": record.id,
#                 "refer": record.refer,
#                 "checkin": record.checkin.strftime('%Y-%m-%d') if isinstance(record.checkin, datetime.date) else record.checkin,
#                 "checkout": record.checkout.strftime('%Y-%m-%d') if isinstance(record.checkout, datetime.date) else record.checkout,
#                 "totalGuest": record.totalGuest,
#                 "totalChildren": record.totalChildren,
#                 "totalInfants": record.totalInfants,
#                 "rooms": record.rooms,
#                 "roomGross": record.roomGross,
#                 "state": record.state, 
#             }

#         else:
#             return Response("Invalid type", content_type='text/plain', status=400)

#         return Response(json.dumps(response_data), content_type='application/json')
# *******************************PSEUDOCODICE PER Integrare questa parte nell'IF relativo a RESERVATION_CREATED*******************************
# from odoo import http
# from odoo.http import request, Response
# import json
# import datetime


# class RoomBookingController(http.Controller):

#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         data_dict = json.loads(json_data)
#         content = json.loads(data_dict.get("content"))

#         if not content.get("refer") or not content.get("guests"):
#             return Response("Missing required fields", content_type='text/plain', status=400)

#         checkin_str = content.get("guests")[0].get("checkin")
#         checkout_str = content.get("guests")[0].get("checkout")
        
#         try:
#             checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
#             checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
#         except ValueError:
#             return Response("Invalid date format", content_type='text/plain', status=400)

#         reservation_data = {
#             'refer': content.get("refer"),
#             'checkin': checkin_date,
#             'checkout': checkout_date,
#             'totalGuest': content.get("totalGuest"),
#             'totalChildren': content.get("totalChildren"),
#             'totalInfants': content.get("totalInfants"),
#             'rooms': content.get("rooms"),
#             'roomGross': content.get("roomGross")
#         }

#         product_type = data_dict.get("type")
#         response_data = self.calculate_response_data(reservation_data, product_type)

#         if data_dict.get("type") == "RESERVATION_CREATED":
#             invoice_response = self.create_invoice(reservation_data)
#             response_data.update(invoice_response)

#         return Response(json.dumps(response_data), content_type='application/json', status=200)
# # account_id
#     def create_invoice(self, reservation_data):
#         invoice_details = self.calculate_invoice_details(reservation_data)

#         invoice_values = {
#             'refer': reservation_data['refer'],
#             'checkin': reservation_data['checkin'],
#         }

#         invoice_record = request.env['account.move'].sudo().create(invoice_values)

#         # Assuming an example account_id (e.g., 42). You should replace it with the actual account id you want to use.
#         actual_account_id = 44

#         # Create booking detail line
#         booking_line_values = {
#             'move_id': invoice_record.id,
#             'name': invoice_details['booking_name'],
#             'quantity': invoice_details['booking_quantity'], 
#             'price_unit': invoice_details['booking_price_unit'],
#             'account_id': actual_account_id
#         }
#         booking_line_record = request.env['account.move.line'].sudo().create(booking_line_values)

#         # Create tourist tax line
#         tourist_tax_line_values = {
#             'move_id': invoice_record.id,
#             'name': "Tassa soggiorno",
#             'quantity': invoice_details['tourist_tax_quantity'], 
#             'price_unit': 2,
#             'account_id': actual_account_id
#         }
#         tourist_tax_line_record = request.env['account.move.line'].sudo().create(tourist_tax_line_values)

#         return {
#             'invoice_id': invoice_record.id,
#             'booking_line_id': booking_line_record.id,
#             'tourist_tax_line_id': tourist_tax_line_record.id
#         }


#     def calculate_response_data(self, reservation_data, product_type):
#         if product_type == "Tassa soggiorno":
#             return self._calculate_tourist_tax(reservation_data)
#         elif product_type == "PERNOTTO":
#             return self._calculate_booking_details(reservation_data)
#         else:
#             raise ValueError(f"Tipo di prodotto non riconosciuto: {product_type}")


#     def calculate_invoice_details(self, reservation_data):
#         checkin_date = reservation_data['checkin']
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days
#         num_ospiti = reservation_data['totalGuest']

#         tourist_tax_quantity = num_notti * num_ospiti
        
#         booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
#         booking_quantity = reservation_data['rooms']
#         booking_price_unit = reservation_data['roomGross']

#         return {
#             "tourist_tax_quantity": tourist_tax_quantity,
#             "booking_name": booking_name,
#             "booking_quantity": booking_quantity,
#             "booking_price_unit": booking_price_unit
            
#     }
# *******************************JSON COMPRENSIVO DEI DATI RELATIVI A TASSA SOGGIORNO E PERNOTTO*******************************
# from odoo import http
# from odoo.http import request, Response
# import json
# import datetime


# class RoomBookingController(http.Controller):

#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         data_dict = json.loads(json_data)
#         content = json.loads(data_dict.get("content"))

#         if not content.get("refer") or not content.get("guests"):
#             return Response("Missing required fields", content_type='text/plain', status=400)

#         checkin_str = content.get("guests")[0].get("checkin")
#         checkout_str = content.get("guests")[0].get("checkout")
        
#         try:
#             checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
#             checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
#         except ValueError:
#             return Response("Invalid date format", content_type='text/plain', status=400)

#         reservation_data = {
#             'refer': content.get("refer"),
#             'checkin': checkin_date,
#             'checkout': checkout_date,
#             'totalGuest': content.get("totalGuest"),
#             'totalChildren': content.get("totalChildren"),
#             'totalInfants': content.get("totalInfants"),
#             'rooms': content.get("rooms"),
#             'roomGross': content.get("roomGross")
#         }

#         event_type = data_dict.get("type")
#         response_data = {}

#         if event_type == "RESERVATION_CREATED":
#             invoice_response = self.calculate_invoice_details(reservation_data)
#             response_data.update(invoice_response)

#         return Response(json.dumps(response_data), content_type='application/json', status=200)


#     # def create_invoice(self, reservation_data):
#     #     invoice_details = self.calculate_invoice_details(reservation_data)

#     #     invoice_values = {
#     #         'refer': reservation_data['refer'],
#     #         'checkin': reservation_data['checkin'],
#     #     }

#     #     invoice_record = request.env['account.move'].sudo().create(invoice_values)

#     #     actual_account_id = 44  # Assumed example account ID

#     #     # Create booking detail line
#     #     booking_line_values = {
#     #         'move_id': invoice_record.id,
#     #         'name': invoice_details['booking_name'],
#     #         'quantity': invoice_details['booking_quantity'],
#     #         'price_unit': invoice_details['booking_price_unit'],
#     #         'account_id': actual_account_id
#     #     }
#     #     booking_line_record = request.env['account.move.line'].sudo().create(booking_line_values)

#         # Create tourist tax line
#         # tourist_tax_line_values = {
#         #     'move_id': invoice_record.id,
#         #     'name': "Tassa soggiorno",
#         #     'quantity': invoice_details['tourist_tax_quantity'],
#         #     'price_unit': 2,
#         #     'account_id': actual_account_id
#         # }
#         # tourist_tax_line_record = request.env['account.move.line'].sudo().create(tourist_tax_line_values)

#         # return {
#         #     'invoice_id': invoice_record.id,
#         #     'booking_line_id': booking_line_record.id,
#         #     'tourist_tax_line_id': tourist_tax_line_record.id
#         # }

#     def calculate_invoice_details(self, reservation_data):
#         checkin_date = reservation_data['checkin']
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days
#         num_ospiti = reservation_data['totalGuest']

#         tourist_tax_quantity = num_notti * num_ospiti *2
        
#         booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
#         booking_quantity = reservation_data['rooms']
#         booking_price_unit = reservation_data['roomGross']

    
#         return {
#             "Valore tassa turistica": tourist_tax_quantity,
#             "Identificativo della prenotazione": booking_name,
#             "Numero stanze": booking_quantity,
#             "Costo stanza": booking_price_unit
#         }

# ********************************************new code for generating invoices in odoo*************************************
from odoo import http
from odoo import _
from odoo.http import request, Response
import json
import datetime

class RoomBookingController(http.Controller):

    @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
    def handle_custom_endpoint(self, **post):
        json_data = request.httprequest.data
        data_dict = json.loads(json_data)
        content = json.loads(data_dict.get("content"))

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
            'refer': content.get("refer"),
            'checkin': checkin_date,
            'checkout': checkout_date,
            'totalGuest': content.get("totalGuest"),
            'totalChildren': content.get("totalChildren"),
            'totalInfants': content.get("totalInfants"),
            'rooms': content.get("rooms"),
            'roomGross': content.get("roomGross")
        }

        event_type = data_dict.get("type")
        response_data = {}

        if event_type == "RESERVATION_CREATED":
            invoice_details = self.calculate_invoice_details(reservation_data)
            self.create_invoice(reservation_data, invoice_details)
            response_data.update(invoice_details)
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
            
            response_data = {
                "move_id": invoice_record.id,
                "refer": invoice_record.refer,
                "checkin": invoice_record.checkin.strftime('%Y-%m-%d') if isinstance(invoice_record.checkin, datetime.date) else invoice_record.checkin,
                "checkout": invoice_record.checkout.strftime('%Y-%m-%d') if isinstance(invoice_record.checkout, datetime.date) else invoice_record.checkout,
                "totalGuest": invoice_record.totalGuest,
                "totalChildren": invoice_record.totalChildren,
                "totalInfants": invoice_record.totalInfants,
                "rooms": invoice_record.rooms,
                "roomGross": invoice_record.roomGross,
                "state": invoice_record.state, 
            }

        else:
            return Response("Invalid event type", content_type='text/plain', status=400)
        
        return Response(json.dumps(response_data), content_type='application/json', status=200)

    def calculate_invoice_details(self, reservation_data):
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        num_ospiti = reservation_data['totalGuest']

        tourist_tax_quantity = num_notti * num_ospiti * 2
        
        booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
        booking_quantity = reservation_data['rooms']
        booking_price_unit = reservation_data['roomGross']
    
        return {
            "Valore tassa turistica": tourist_tax_quantity,
            "Identificativo della prenotazione": booking_name,
            "Numero stanze": booking_quantity,
            "Costo stanza": booking_price_unit
        }

    def create_invoice(self, reservation_data, invoice_details):
        # INIZIO RETTIFICA
        pernotto_product = request.env['product.product'].sudo().search([('name', '=', 'Pernotto')], limit=1)
        if not pernotto_product:
            pernotto_product = request.env['product.product'].sudo().create({
                'name': 'Pernotto',
                'type': 'service',
            })

        # tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
        # if not tassa_soggiorno_product:
        #     tassa_soggiorno_product = request.env['product.product'].sudo().create({
        #         'name': 'Tassa di Soggiorno',
        #         'type': 'service',
        #     })

        tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
        if not tassa_soggiorno_product:
            # Cerca un'imposta con tasso 0%
            tax_0_percent = request.env['account.tax'].sudo().search([('amount_type', '=', 'percent'), ('type_tax_use', '=', 'sale'), ('amount', '=', 0)], limit=1)
            
            # Se non trova un'imposta al 0%, solleva un'eccezione.
            if not tax_0_percent:
                raise ValueError("Non esiste un'imposta al 0% nel sistema. Creala o assegnala manualmente.")
            
            vals = {
                'name': 'Tassa di Soggiorno',
                'type': 'service'
            }
            
            if tax_0_percent:
                vals['taxes_id'] = [(6, 0, [tax_0_percent.id])]  # Assegna l'imposta trovata al prodotto

            tassa_soggiorno_product = request.env['product.product'].sudo().create(vals)

    
        # FINE RETTIFICA
        customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 44
        journal_id = customer_invoice_journal.id
        
        
        invoice_values = {
            'journal_id': journal_id,
            'move_type': 'out_invoice',
            # 'partner_id': 1, # Example partner_id. In reality, this should be taken from reservation_data or elsewhere.
            'checkin': reservation_data['checkin'],
            'checkout': reservation_data['checkout'],
            'refer': reservation_data['refer'],
            'totalGuest': reservation_data['totalGuest'],
            'totalChildren': reservation_data['totalChildren'],
            'rooms': reservation_data['rooms'],
            'roomGross': reservation_data['roomGross'],

            
        }

        invoice_record = request.env['account.move'].sudo().create(invoice_values)

        # Create booking detail line
        booking_line_values = {
            'move_id': invoice_record.id,
            'product_id': pernotto_product.id,
            'name': invoice_details['Identificativo della prenotazione'],
            'quantity': invoice_details['Numero stanze'],
            'price_unit': invoice_details['Costo stanza'],
            'account_id': account_id
            # 'account_id': 44  # Assumed account ID, you should replace with the actual account id for this transaction type
        }
        request.env['account.move.line'].sudo().create(booking_line_values)

        # Create tourist tax line
        tourist_tax_line_values = {
            'move_id': invoice_record.id,
            'product_id': tassa_soggiorno_product.id,
            'name': "Tassa soggiorno",
            'quantity': 1,  # Assuming the tax is a fixed amount per reservation
            'price_unit': invoice_details['Valore tassa turistica'],
            'account_id': account_id
            # 'account_id': 44  # Assumed account ID, you should replace with the actual account id for this transaction type
        }
        request.env['account.move.line'].sudo().create(tourist_tax_line_values)
    






