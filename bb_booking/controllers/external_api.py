from odoo import http
from odoo.http import request, Response
from odoo.tools.safe_eval import json
from werkzeug.wrappers import Response
import datetime
#*****************************************QUESTO CODICE FUNZIONA NELLA GENERAZIONE DELLE RISPOSTE IN POSTMAN*****************


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
from odoo import http
from odoo.http import request, Response
from odoo.tools.safe_eval import json
import datetime

class RoomBookingController(http.Controller):
    @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
    def handle_custom_endpoint(self, **post):
        json_data = request.httprequest.data
        try:
            data_dict = json.loads(json_data)
            content = json.loads(data_dict.get("content"))
            type = data_dict.get("type")  # assuming that "type" is the type of operation to perform
        except ValueError:
            return Response("Errore nella formattazione dei dati JSON", content_type='text/plain', status=400)

        reservation_data = {
            'refer': content.get("refer"),
            'checkin': content.get("guests")[0].get("checkin"),
            'checkout': content.get("guests")[0].get("checkout"),
            'totalGuest': content.get("totalGuest"),
            'totalChildren': content.get("totalChildren"),
            'totalInfants': content.get("totalInfants"),
            'rooms': content.get("rooms"),
            'roomGross': content.get("roomGross")
        }

        try:
            model = 'account.move'  # replace with the actual name of your booking model

            if type == 'RESERVATION_CREATED':
                reservation_data['state'] = 'draft'
                new_move = request.env[model].sudo().create(reservation_data)
                response_data = {
                    "move_id": new_move.id,
                    "refer": new_move.refer,
                    "checkin": new_move.checkin.strftime('%Y-%m-%d') if isinstance(new_move.checkin, datetime.date) else new_move.checkin,
                    "checkout": new_move.checkout.strftime('%Y-%m-%d') if isinstance(new_move.checkout, datetime.date) else new_move.checkout,
                    "totalGuest": new_move.totalGuest,
                    "totalChildren": new_move.totalChildren,
                    "totalInfants": new_move.totalInfants,
                    "rooms": new_move.rooms,
                    "roomGross": new_move.roomGross,
                    "state": new_move.state,  # Assuming that 'state' field exists in your model
                }

            elif type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
                refer_id = reservation_data.get('refer')
                record = request.env[model].sudo().search([('refer', '=', refer_id)])
                if not record:
                    return Response("No reservation found with the provided refer ID", content_type='text/plain', status=400)

                new_state = 'cancelled' if type == 'RESERVATION_CANCELLED' else 'confirmed'
                record.sudo().write({'state': new_state})
                response_data = {
                    "move_id": record.id,
                    "refer": record.refer,
                    "checkin": record.checkin.strftime('%Y-%m-%d') if isinstance(record.checkin, datetime.date) else record.checkin,
                    "checkout": record.checkout.strftime('%Y-%m-%d') if isinstance(record.checkout, datetime.date) else record.checkout,
                    "totalGuest": record.totalGuest,
                    "totalChildren": record.totalChildren,
                    "totalInfants": record.totalInfants,
                    "rooms": record.rooms,
                    "roomGross": record.roomGross,
                    "state": record.state,  # Assuming that 'state' field exists in your model
                }

            else:
                return Response("Invalid type", content_type='text/plain', status=400)

        except Exception as e:
            return Response(str(e), content_type='text/plain', status=500)

        return Response(json.dumps(response_data), content_type='application/json')


#
#                 if type == 'RESERVATION_CREATED':
#
#                     fields['state'] = 'draft'
#                     record = request.env[model].create(response_data)
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


# import requests

# url = "http://localhost:8069/api/test"

# payload = "{\r\n  \"content\": \"{\\\"cancelPenality\\\":-1,\\\"cityTaxZero\\\":false,\\\"extraIncluded\\\":[],\\\"json\\\":{},\\\"loyaltyDiscount\\\":false,\\\"refer\\\":\\\"DH9SC0\\\",\\\"channelId\\\":288,\\\"channelRefer\\\":\\\"DH9SC0\\\",\\\"status\\\":\\\"CONFIRMED\\\",\\\"checkin\\\":\\\"2023-10-12T10:00:00Z[UTC]\\\",\\\"checkout\\\":\\\"2023-10-12T22:00:00Z[UTC]\\\",\\\"createTime\\\":\\\"2023-10-12T13:36:11Z[UTC]\\\",\\\"updateTime\\\":\\\"2023-10-12T13:36:21Z[UTC]\\\",\\\"children\\\":0,\\\"guests\\\":[{\\\"checkin\\\":\\\"2023-10-12\\\",\\\"checkout\\\":\\\"2023-10-13\\\",\\\"city\\\":\\\"\\\",\\\"email\\\":\\\"Van@octorate.com\\\",\\\"familyName\\\":\\\"Gogh\\\",\\\"givenName\\\":\\\"Van\\\",\\\"language\\\":\\\"EN\\\",\\\"phone\\\":\\\"\\\",\\\"source\\\":\\\"USER\\\",\\\"type\\\":\\\"BOOKER\\\"}],\\\"infants\\\":0,\\\"phone\\\":\\\"\\\",\\\"roomGross\\\":500.00,\\\"totalGross\\\":500.00,\\\"totalGuest\\\":2,\\\"accommodation\\\":{\\\"address\\\":\\\"via filippo caruso\\\",\\\"checkinEnd\\\":20,\\\"checkinStart\\\":12,\\\"checkout\\\":12,\\\"city\\\":\\\"ROMA\\\",\\\"currency\\\":\\\"EUR\\\",\\\"id\\\":\\\"557782\\\",\\\"latitude\\\":41.8489657,\\\"longitude\\\":12.5764685,\\\"name\\\":\\\"OdooERP  Test Api Building L.A.\\\",\\\"phoneNumber\\\":\\\"+3906060606\\\",\\\"timeZone\\\":\\\"Europe/Rome\\\",\\\"timeZoneOffset\\\":\\\"+01:00\\\",\\\"zipCode\\\":\\\"00173\\\"},\\\"arrivalTime\\\":\\\"12:00:00\\\",\\\"autoLoginParam\\\":\\\"4974220ddc3d23ff1670a7a5f09eb5ee96a86b50d200198f113c29dc326905422a9454108c21ea68408fb0598352d8f4\\\",\\\"channelName\\\":\\\"octoevo autosubmit\\\",\\\"currency\\\":\\\"EUR\\\",\\\"firstName\\\":\\\"Van\\\",\\\"freeCancellation\\\":true,\\\"grouped\\\":false,\\\"guestMailAddress\\\":\\\"Van@octorate.com\\\",\\\"guestsList\\\":\\\"Van Gogh\\\",\\\"id\\\":104805148,\\\"itemCompleted\\\":false,\\\"lastName\\\":\\\"Gogh\\\",\\\"noShow\\\":false,\\\"paymentStatus\\\":\\\"UNPAID\\\",\\\"paymentType\\\":\\\"UNKNOWN\\\",\\\"payments\\\":[],\\\"priceBreakdown\\\":[{\\\"type\\\":\\\"DAILY_ROOM_PRICE\\\",\\\"name\\\":null,\\\"createTime\\\":null,\\\"day\\\":\\\"2023-10-11T22:00:00Z[UTC]\\\",\\\"price\\\":500.00,\\\"reference\\\":\\\"63880004\\\",\\\"externalId\\\":null,\\\"included\\\":true,\\\"product\\\":null,\\\"quantity\\\":null},{\\\"type\\\":\\\"ROOM_NET\\\",\\\"name\\\":null,\\\"createTime\\\":null,\\\"day\\\":null,\\\"price\\\":500.00,\\\"reference\\\":null,\\\"externalId\\\":null,\\\"included\\\":true,\\\"product\\\":null,\\\"quantity\\\":null},{\\\"type\\\":\\\"VAT\\\",\\\"name\\\":null,\\\"createTime\\\":null,\\\"day\\\":null,\\\"price\\\":0.00,\\\"reference\\\":null,\\\"externalId\\\":null,\\\"included\\\":true,\\\"product\\\":null,\\\"quantity\\\":null}],\\\"product\\\":599456,\\\"roomName\\\":\\\"Building Los Angeles Apartment 101\\\",\\\"roomNameGuest\\\":\\\"Building Los Angeles Apartment 101\\\",\\\"rooms\\\":1,\\\"totalChildren\\\":0,\\\"totalInfants\\\":0,\\\"totalPaid\\\":0.00,\\\"touristTax\\\":0}\",\r\n  \"createTime\": \"2023-10-12T13:37:19Z[UTC]\",\r\n  \"hmac\": \"2837dcafd33f71a30967dc4d955319b07abfa45f\",\r\n  \"id\": 63000829,\r\n  \"nextTry\": \"2023-10-12T13:42:20.2Z[UTC]\",\r\n  \"reference\": \"104805148\",\r\n  \"retry\": 10,\r\n  \"subscription\": {\r\n    \"apiMember\": 578,\r\n    \"createTime\": \"2023-09-20T15:11:49Z[UTC]\",\r\n    \"enabled\": true,\r\n    \"endpoint\": \"https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd\",\r\n    \"id\": 1179,\r\n    \"priority\": 1,\r\n    \"processTime\": \"2023-10-12T13:37:19Z[UTC]\",\r\n    \"type\": \"RESERVATION_CREATED\"\r\n  },\r\n  \"type\": \"RESERVATION_CREATED\"\r\n}"
# headers = {}

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)
