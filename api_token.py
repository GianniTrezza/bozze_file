# import requests
# from odoo import http, models, fields, api
# from odoo.http import request
import json
# from odoo import http

from odoo import http
from odoo.http import request
import requests
import logging

CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

def get_access_token_basic():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    response = requests.post(endpoint, data=payload, headers=headers)
    return response.json().get("access_token", None)

def get_access_token_full():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"
    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": "d2137ad53d6648bab1e62d88b0586ef09514ccb644344b44a8dd4ba748f5d6a9",
        "grant_type": "authorization_code",
        "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
    }
    response = requests.post(endpoint, data=payload, headers=headers)
    print(response.status_code)
    print(response.json())  
    return response.json().get("access_token", None)


def fetch_accommodations(token):
    endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

def choose_accommodation(accommodations):
    print("Scegli un accommodation:")
    for index, accommodation in enumerate(accommodations, start=1):
        print(f"{index}. {accommodation.get('name', 'Nome non disponibile')} (ID: {accommodation.get('id', 'ID non disponibile')})")
    choice = int(input("Inserisci il numero corrispondente all'accommodation: "))
    return accommodations[choice-1].get("id")
# PRELIEVO DELLE RESERVATIONS SENZA FILTRI
def fetch_reservations(token, accommodation_id):
    endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

#PRELIEVO DELLE RESERVATIONS CON FILTRI
# def fetch_reservations(token, accommodation_id):
#     endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
#     response = requests.get(endpoint, headers=headers)

#     # Printing raw data for debugging
#     print(response.text)

#     reservations = response.json()

#     # Check if reservations is a list, if not, try to extract from a 'data' key or set it to an empty list
#     if not isinstance(reservations, list):
#         reservations = reservations.get('data', [])

#     # Process the reservations
#     processed_reservations = [
#         {
#             'checkin': reservation.get('checkin') if isinstance(reservation, dict) else json.loads(reservation).get('checkin'),
#             'checkout': reservation.get('checkout') if isinstance(reservation, dict) else json.loads(reservation).get('checkout'),
#             'totalChildren': reservation.get('totalChildren') if isinstance(reservation, dict) else json.loads(reservation).get('totalChildren'),
#             'totalInfants': reservation.get('totalInfants') if isinstance(reservation, dict) else json.loads(reservation).get('totalInfants'),
#             'totalGuest': reservation.get('totalGuest') if isinstance(reservation, dict) else json.loads(reservation).get('totalGuest'),
#             'totalGross': reservation.get('totalGross') if isinstance(reservation, dict) else json.loads(reservation).get('totalGross'),
#             'roomGross': reservation.get('roomGross') if isinstance(reservation, dict) else json.loads(reservation).get('roomGross'),
            
#         }
#         for reservation in reservations
#     ]

#     return processed_reservations
access_token_basic = get_access_token_basic()
access_token_full = get_access_token_full()
print(f"Ecco il token con grant parziale:{access_token_basic}")
print(f"Ecco il token con grant completo:{access_token_full}")

accommodations = fetch_accommodations(access_token_basic)

accommodation_id = choose_accommodation(accommodations)

reservations = fetch_reservations(access_token_full, accommodation_id)
print(f"Ecco le prenotazioni relative a {accommodation_id}: {reservations}")

# RESERVATIONS FILTRATE
# reservations = fetch_reservations(access_token_full, accommodation_id)
# for reservation in reservations:
#     print("---------- Prenotazione Inizio ----------")
    
#     print(f"Check-in: {reservation['checkin']}")
#     print(f"Check-out: {reservation['checkout']}")
#     print(f"Numero totali di bambini: {reservation['totalChildren']}")
#     print(f"Numero totali di neonati: {reservation['totalInfants']}")
#     print(f"Numero totali di ospiti: {reservation['totalGuest']}")
#     print(f"Costo Stanza: {reservation['roomGross']}")
#     print(f"Costo Totale: {reservation['totalGross']}")
    
#     print("---------- Prenotazione Fine ----------")


def fetch_webhooks(access_token_full):
    endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token_full}"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
        return []

    return response.json()
# FUNZIONE CHE TI CONSENTE DI SCEGLIERE TRA GLI EVENTS COSICCHé TU POSSA MANDARE I DATI RELATIVI AL WEBHOOK CIASCUN EVENT ALLA VOLTA
# def choose_event():
#     EVENTS = [
#         "RESERVATION_CREATED", "RESERVATION_CHANGE", "RESERVATION_CANCELLED", "RESERVATION_CONFIRMED",
#         "CONTENT_NOTIFICATION", "CONTENT_PUSH", "PORTAL_SUBSCRIPTION_CALENDAR",
#         "XXX_NOT_USED_PORTAL_PROCESS_FAILED", "CHAT_MESSAGE_RECEIVED"
#     ]
#     print("Scegli un evento per configurare il webhook:")
#     for index, event in enumerate(EVENTS, start=1):
#         print(f"{index}. {event}")
#     choice = int(input("Inserisci il numero corrispondente all'evento: "))
#     return EVENTS[choice-1]

# webhook_url = "https://webhook.site/7562c12d-e21c-402c-8faa-b6c08e9e564d"
webhook_url="https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"

# Ottieni i webhooks configurati
 # Assicurati di avere un access token valido
webhooks = fetch_webhooks(access_token_full)
print(f"Ecco una lista di possibili webhook:{webhooks}")

# event_to_add = choose_event()

# print(event_to_add)
# url_to_add = "https://webhook.site/#!/e2e61afa-8888-487d-a8d6-4c79156487dd"

# Invia i dati al webhook
# for webhook_data in webhooks:
#     response = requests.post(webhook_url, json=webhook_data)
#     if response.status_code == 200:
#         print(f"Dati inviati con successo al webhook: {webhook_url}")
#     else:
#         print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")

# SPUNTI PER DOMANI
# ODOO_WEBHOOK_URL = "http://localhost:8069/room_booking/webhook"

# for reservation in reservations:
#     requests.post(ODOO_WEBHOOK_URL, json=reservation)


# QUESTO SNIPPET FUNZIONA NELL'INVIARE I DATI DI PRENOTAZIONE AL WEBHOOK, MA NON è INTEGRATO CON ODOO
class RoomBookingController(http.Controller):

    @http.route('/room_booking/webhook', type='json', auth='public', methods=['POST'])
    def receive_data(self, **kw):
        data = request.jsonrequest
        event_type = data.get('type')  # Corretto da 'eventType' a 'type'
        webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"

        headers = {
            'Content-Type': 'application/json'
        }

        response_message = {"message": "Event not supported"}

        if event_type == "RESERVATION_CREATED":
            # Logica per la gestione della creazione di una nuova prenotazione.
            reservation = request.env['bb_booking.roombooking'].sudo().create({
                'refer': data.get('reservation_id'),
                # 'checkin': data.get('checkin'),
                # 'checkout': data.get('checkout'),
                # 'totalChildren': data.get('totalChildren'),
                # 'totalInfants': data.get('totalInfants'),
                # 'totalGuest': data.get('totalGuest'),
                # 'roomGross': data.get('roomGross'),
                # 'totalGross': data.get('totalGross'),
                # Aggiungi altri campi qui se necessario
            })

            # Invia i dati al webhook
            try:
                response = requests.post(webhook_url, json=data, headers=headers)  # Qui includiamo gli headers
                if response.status_code == 200:
                    response_message = {"message": "Reservation created and data sent to webhook"}
                else:
                    response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
            except requests.RequestException as e:
                response_message = {"message": f"Request failed: {str(e)}"}

        elif event_type == "RESERVATION_CANCELLED":
            # Trova il record di prenotazione corrispondente e aggiorna il campo 'refer'
            reservation_id = data.get('reservation_id')
            # reservation = request.env['bb_booking.roombooking'].sudo().search([('id', '=', reservation_id)])
            reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

            if reservation:
                # Aggiorna il campo 'refer' a "Cancellato"
                # reservation.write({'refer': 'Cancellato'})
                reservation.write({'status': 'Cancellato'})

                # Invia i dati al webhook
                try:
                    response = requests.post(webhook_url, json=data, headers=headers)  # Qui includiamo gli headers
                    if response.status_code == 200:
                        response_message = {"message": "Reservation cancelled and data sent to webhook"}
                    else:
                        response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
                except requests.RequestException as e:
                    response_message = {"message": f"Request failed: {str(e)}"}

        elif event_type == "RESERVATION_CONFIRMED":
            # Trova il record di prenotazione corrispondente e aggiorna il campo 'refer'
            reservation_id = data.get('reservation_id')
            # reservation = request.env['bb_booking.roombooking'].sudo().search([('id', '=', reservation_id)])
            reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

            if reservation:
                # Aggiorna il campo 'refer' a "Confermato"
                # reservation.write({'refer': 'Confermato'})
                reservation.write({'status': 'Confermato'})

                # Invia i dati al webhook
                try:
                    response = requests.post(webhook_url, json=data, headers=headers)  # Qui includiamo gli headers
                    if response.status_code == 200:
                        response_message = {"message": "Reservation confirmed and data sent to webhook"}
                    else:
                        response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
                except requests.RequestException as e:
                    response_message = {"message": f"Request failed: {str(e)}"}

        return response_message



# _logger = logging.getLogger(__name__)
# _logger.info("Un messaggio informativo")
# _logger.error("Messaggio di errore")

# # 'checkin': data.get('checkin'),
# #                 # 'checkout': data.get('checkout'),



# class RoomBookingController(http.Controller):
#     @http.route('/room_booking/webhook', type='json', auth='public', methods=['POST'])
#     def receive_data(self, **kw):
#         data = request.jsonrequest
#         event_type = data.get('type')  # Corretto da 'eventType' a 'type'
#         webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"

#         headers = {
#             'Content-Type': 'application/json'
#         }

#         response_message = {"message": "Event not supported"}

#         if event_type == "RESERVATION_CREATED":
#             # Logica per la gestione della creazione di una nuova prenotazione.
#             try:
#                 reservation = request.env['bb_booking.roombooking'].sudo().create({
#                     'checkin': data.get('checkin'),
#                     'checkout': data.get('checkout'),
#                     # 'refer': data.get('reservation_id'),
#                     # Aggiungi altri campi qui se necessario
#                 })

#                 # Invia i dati al webhook
#                 response = requests.post(webhook_url, json=data, headers=headers)
#                 if response.status_code == 200:
#                     response_message = {"message": "Reservation created and data sent to webhook"}
#                 else:
#                     response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#             except Exception as e:
#                 response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CANCELLED":
#             reservation_id = data.get('reservation_id')
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 try:
#                     # Aggiorna il campo 'status' a "Cancellato"
#                     reservation.write({'status': 'Cancellato'})

#                     # Invia i dati al webhook
#                     response = requests.post(webhook_url, json=data, headers=headers)
#                     _logger.info(f"Data received: {data}")
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation cancelled and data sent to webhook"}
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except Exception as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CONFIRMED":
#             # Trova il record di prenotazione corrispondente e aggiorna il campo 'status'
#             reservation_id = data.get('reservation_id')
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 try:
#                     # Aggiorna il campo 'status' a "Confermato"
#                     reservation.write({'status': 'Confermato'})

#                     # Invia i dati al webhook
#                     response = requests.post(webhook_url, json=data, headers=headers)
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation confirmed and data sent to webhook"}
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except Exception as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         return response_message





 

# def get_refreshed_token(refresh_token):
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/refresh"
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "refresh_token": refresh_token,
#         "grant_type": "refresh_token"
#     }

#     response = requests.post(endpoint, data=payload, headers=headers)
#     if response.status_code == 200:
#         return response.json().get("access_token", None)
#     else:
#         print(f"Errore: {response.status_code} - {response.text}")
#         return None

# refresh_token = "2acf003360ea4ebca6871b5d7e56efe2"
# new_access_token = get_refreshed_token(refresh_token)
# print(f"Nuovo token di accesso: {new_access_token}")

