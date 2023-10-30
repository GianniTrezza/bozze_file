
# INIZIO CODICE USATO
import requests
import json


# Dati del client per ottenere il token
CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"


# Funzione per ottenere il token di accesso
def get_access_token():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(endpoint, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
        return None


# Ottieni il token di accesso
access_token = get_access_token()
if access_token:
    print(f"Token di accesso ottenuto con successo: {access_token}")
else:
    print("Errore nell'ottenere il token di accesso.")


def get_access_token2():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "authorization_code",
        "code": "dddfa915b82342a685779bfc51cd848c29e70b0af6be4108bd08f95684f4c013",
        "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
        "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
        "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
    }

    response = requests.post(endpoint, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
        return None


# Ottieni il token di accesso
access_token_a = get_access_token2()

if access_token_a:
    print(f"Token per visionare le reservation è : {access_token_a}")
else:
    print("Errore nell'ottenere il token di accesso.")


def refresh_token():
   endpoint = "https://api.octorate.com/connect/rest/v1/identity/refresh"

   headers = {
       "Accept": "application/json",
       "Content-Type": "application/x-www-form-urlencoded"
   }

   payload = {
                "grant_type": "authorization_code",
                "code": "503f2ac0499943cdab59b3eab796b5c3b62db49ff34146ff842abd685d77b73d",
               "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
               "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
                "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html",
                'refresh_token': '2acf003360ea4ebca6871b5d7e56efe2'
   }

   response = requests.post(endpoint, data=payload, headers=headers)

   if response.status_code == 200:
       print("refresh avvenuto con successo")
       return response.json().get("access_token")
   else:
       print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
       return None


def fetch_accommodations(token):
    endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
    # print(token)

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore nell'ottenere gli accommodation: {response.headers}, {headers}")
        return []


# Esempio di utilizzo:
# Ottieni il token di accesso (già ottenuto precedentemente)
access_token = get_access_token()
# Ottenere gli accommodation
accommodations = fetch_accommodations(access_token)
if accommodations:
    print(f"Gli accommodation ottenuti con successo: {accommodations}")
else:
    print("Nessun accommodation disponibile o errore nell'ottenimento.")


def fetch_reservations_for_accommodation_id(access_token_a, accommodation_id):
    reservation_endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token_a}"
    }
    response = requests.get(reservation_endpoint, headers=headers)

    if response.status_code == 200:
        reservations = response.json()
        return reservations
    else:
        print(
            f"Errore nell'ottenere le prime prenotazioni per l'alloggio {accommodation_id}, {headers}, {response.status_code}, {response.text}")
        return []


# Esempio di utilizzo:
# Ottieni il token di accesso (già ottenuto precedentemente)

# access_token_a = get_access_token2()
# print(access_token_a)
# Inserisci l'ID dell'alloggio per cui desideri ottenere le prenotazioni
accommodation_id = "632966"

# Ottieni le prenotazioni per l'alloggio selezionato utilizzando il token ottenuto
reservations = fetch_reservations_for_accommodation_id(access_token_a, accommodation_id)

# Controlla se ci sono prenotazioni
if reservations:
    print(f"{accommodation_id}: {reservations}")

    # Converti le prenotazioni in formato JSON
    reservations_json = json.dumps(reservations)

    # Definisci l'URL del webhook al quale inviare le prenotazioni
    webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"

    # Invia i dati al webhook
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, data=reservations_json, headers=headers)

    # Verifica la risposta del webhook
    if response.status_code == 200:
        print("Dati inviati con successo al webhook.")
    else:
        print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")
else:
    print("Nessuna prenotazione disponibile o errore nell'ottenimento.")

print(f"{accommodation_id}:{reservations}")



def fetch_webhooks(access_token_a):
    endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token_a}"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
        return []

    return response.json()



# FINE CODICE USATO
# def create_subscription(event_type, access_token_a):
#     # URL per il tipo di evento specifico
#     subscription_url = f"https://api.octorate.com/connect/rest/v1/subscription/{event_type}"
#     print(subscription_url)
#     # URL dell'endpoint a cui verranno inviati i webhook
#    # endpoint_url = "https://webhook.site/7562c12d-e21c-402c-8faa-b6c08e9e564d"
#
#     # Crea il payload per la richiesta
#     payload = {
#         "endpoint": webhook_url,
#         #"type": "CONTENT_NOTIFICATION"
#     }
#     print(payload)
#     # Aggiungi l'intestazione di autorizzazione
#     headers = {
#         "Authorization": f"Bearer {access_token_a}",
#         "Content-Type": "application/json"
#     }
#     print(headers)
#     # Invia la richiesta per creare l'abbonamento
#     response = requests.post(subscription_url, json=payload, headers=headers)
#
#     if response.status_code == 200:
#         print(f"Abbonamento per {event_type} creato con successo.")
#     else:
#         print(f"Errore durante la creazione dell'abbonamento per {event_type}: {response.status_code} - {response.text}")
#
# # Assicurati di avere un access token valido
#
#
# # Definisci i tipi di eventi per i quali vuoi creare gli abbonamenti
# event_types = ["RESERVATION_CREATED", "RESERVATION_CHANGE", "RESERVATION_CANCELLED", "RESERVATION_CONFIRMED"]
#
# # Chiamare la funzione per ciascun tipo di evento
# for event_type in event_types:
#     create_subscription(event_type, access_token_a)
#     print("è andata")

# COME GESTIRE IL RIEMPIMENTO DEI CAMPI RELATIVI ALLE PRENOTAZIONI
# from odoo import http
# from odoo.http import request
# import json
# from werkzeug.wrappers import Response

# class RoomBookingController(http.Controller):
#     @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
#     def handle_custom_endpoint(self, **post):
#         json_data = request.httprequest.data
#         try:
#             data_dict = json.loads(json_data)
#             content = json.loads(data_dict.get("content"))

#         except ValueError:
#             return "Errore nella formattazione dei dati JSON"

#         # Estrai i valori necessari dal dizionario dei dati
#         refer = content.get("refer")
#         guestsList = content.get("guestsList")
#         roomGross = content.get("roomGross")
#         totalGuest = content.get("totalGuest")
#         guests = content.get("guests")
#         checkin = guests[0].get("checkin")
#         checkout = guests[0].get("checkout")
#         totalChildren = content.get("totalChildren")  # Aggiungi queste righe per altri dati che vuoi estrarre
#         totalInfants = content.get("totalInfants")
#         rooms = content.get("rooms")

#         # Prepara i dati per il nuovo record
#         vals = {
#             'refer': refer,
#             'checkin': checkin,
#             'checkout': checkout,
#             'totalGuest': totalGuest,
#             'totalChildren': totalChildren,
#             'totalInfants': totalInfants,
#             'rooms': rooms,
#             'roomGross': roomGross,
#             # Aggiungi ulteriori campi qui, se necessario
#         }

#         # Crea un nuovo record nel modello 'account.move'
#         try:
#             new_move = request.env['account.move'].sudo().create(vals)
#         except Exception as e:
#             # Gestisci le eccezioni come preferisci
#             return str(e)

#         # Prepara la risposta
#         response_data = {
#             "refer": refer,
#             "guestsList": guestsList,  # Questo dato non sembra essere salvato nel modello, quindi verrà solo restituito nella risposta
#             "prezzo": roomGross,
#             "ospiti": totalGuest,
#             "checkin": checkin,
#             "checkout": checkout,
#             # Aggiungi altri campi di risposta qui, se necessario
#         }

#         return Response(json.dumps(response_data), content_type='application/json')
# RETTIFICHE external_api.py
# from odoo import http
# from odoo import _
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
#             invoice_details = self.calculate_invoice_details(reservation_data)
#             self.create_invoice(reservation_data, invoice_details)
#             response_data.update(invoice_details)
#         elif event_type == "RESERVATION_CHANGE":
#             refer_id = reservation_data.get('refer')
#             invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
#             if not invoice_record:
#                 return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
#             invoice_record.sudo().write(reservation_data)
#             response_data.update({
#                 "move_id": invoice_record.id,
#                 "state": invoice_record.state,
#             })
#         elif event_type == "RESERVATION_CONFIRMED":
#             refer_id = reservation_data.get('refer')
#             invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
#             if not invoice_record:
#                 return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
#             invoice_record.sudo().write({'state': 'posted'})
#             response_data.update({
#                 "move_id": invoice_record.id,
#                 "state": invoice_record.state,
#             })
#         elif event_type == "RESERVATION_CANCELLED":
#             refer_id = reservation_data.get('refer')
#             invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
#             if not invoice_record:
#                 return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
#             invoice_record.sudo().unlink()
#             response_data.update({"message": "Invoice cancelled"})
#         else:
#             return Response("Invalid event type", content_type='text/plain', status=400)

#         return Response(json.dumps(response_data), content_type='application/json', status=200)

#     def calculate_invoice_details(self, reservation_data):
#         checkin_date = reservation_data['checkin']
#         checkout_date = reservation_data['checkout']
#         delta = checkout_date - checkin_date
#         num_notti = delta.days
#         num_ospiti = reservation_data['totalGuest']
#         tourist_tax_quantity = num_notti * num_ospiti * 2
#         booking_name = f"Prenotazione {reservation_data['refer']} dal {checkin_date} al {checkout_date}"
#         booking_quantity = reservation_data['rooms']
#         booking_price_unit = reservation_data['roomGross']
#         return {
#             "Valore tassa turistica": tourist_tax_quantity,
#             "Identificativo della prenotazione": booking_name,
#             "Numero stanze": booking_quantity,
#             "Costo stanza": booking_price_unit
#         }

#     def create_invoice(self, reservation_data, invoice_details):
#         pernotto_product = request.env['product.product'].sudo().search([('name', '=', 'Pernotto')], limit=1)
#         if not pernotto_product:
#             pernotto_product = request.env['product.product'].sudo().create({
#                 'name': 'Pernotto',
#                 'type': 'service',
#             })
#         tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
#         if not tassa_soggiorno_product:
#             tax_0_percent = request.env['account.tax'].sudo().search([('amount_type', '=', 'percent'), ('type_tax_use', '=', 'sale'), ('amount', '=', 0)], limit=1)
#             if not tax_0_percent:
#                 raise ValueError("Non esiste un'imposta al 0% nel sistema. Creala o assegnala manualmente.")
#             vals = {
#                 'name': 'Tassa di Soggiorno',
#                 'type': 'service'
#             }
#             if tax_0_percent:
#                 vals['taxes_id'] = [(6, 0, [tax_0_percent.id])]
#             tassa_soggiorno_product = request.env['product.product'].sudo().create(vals)
#         customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
#         account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 44
#         journal_id = customer_invoice_journal.id
#         invoice_values = {
#             'journal_id': journal_id,
#             'move_type': 'out_invoice',
#             'checkin': reservation_data['checkin'],
#             'checkout': reservation_data['checkout'],
#             'refer': reservation_data['refer'],
#             'totalGuest': reservation_data['totalGuest'],
#             'totalChildren': reservation_data['totalChildren'],
#             'rooms': reservation_data['rooms'],
#             'roomGross': reservation_data['roomGross'],
#         }
#         invoice_record = request.env['account.move'].sudo().create(invoice_values)
#         booking_line_values = {
#             'move_id': invoice_record.id,
#             'product_id': pernotto_product.id,
#             'name': invoice_details['Identificativo della prenotazione'],
#             'quantity': invoice_details['Numero stanze'],
#             'price_unit': invoice_details['Costo stanza'],
#             'account_id': account_id
#         }
#         request.env['account.move.line'].sudo().create(booking_line_values)
#         tourist_tax_line_values = {
#             'move_id': invoice_record.id,
#             'product_id': tassa_soggiorno_product.id,
#             'name': 'Tassa di Soggiorno',
#             'quantity': invoice_details['Valore tassa turistica'],
#             'price_unit': 1,
#             'account_id': account_id
#         }
#         request.env['account.move.line'].sudo().create(tourist_tax_line_values)



