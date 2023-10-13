# from odoo import http, models, api, fields
# from odoo.http import request
# import requests
# import json



# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

# def get_access_token_basic():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     payload = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
#     response = requests.post(endpoint, data=payload, headers=headers)
#     return response.json().get("access_token", None)

# def get_access_token_full():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"
#     headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "code": "b582284d85f64bcaa92acf562769d7fbb04545365ba84732bd2f3fa159f14ce9",
#         "grant_type": "authorization_code",
#         "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
#     }
#     response = requests.post(endpoint, data=payload, headers=headers)
#     print(response.status_code)
#     print(response.json())  
#     return response.json().get("access_token", None)


# def fetch_accommodations(token):
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
#     response = requests.get(endpoint, headers=headers)
#     return response.json()

# def choose_accommodation(accommodations):
#     print("Scegli un accommodation:")
#     for index, accommodation in enumerate(accommodations, start=1):
#         print(f"{index}. {accommodation.get('name', 'Nome non disponibile')} (ID: {accommodation.get('id', 'ID non disponibile')})")
#     choice = int(input("Inserisci il numero corrispondente all'accommodation: "))
#     return accommodations[choice-1].get("id")
# # PRELIEVO DELLE RESERVATIONS SENZA FILTRI
# def fetch_reservations(token, accommodation_id):
#     endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
#     response = requests.get(endpoint, headers=headers)
#     return response.json()



# def handle_new_booking(booking_data):
#     refer = booking_data.get('refer')
#     if not refer:
#         print("Errore: 'refer' mancante nei dati di prenotazione.")
#         return None

#     accommodation_id = booking_data.get("accommodation")["id"]  # Ottiene l'ID della sistemazione dai dati di prenotazione
#     url = f"https://api.octorate.com/api/v1/accommodations/{accommodation_id}/bookings/"

#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#     }

#     new_booking_data = {
#         "content": json.dumps({
#             "refer": refer,  # questo è l'unico campo che abbiamo nel nuovo set di dati
#         })
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(new_booking_data))
#     if response.status_code == 200:
#         print(f"Prenotazione {refer} gestita correttamente.")
#     else:
#         print(f"Errore nella gestione della prenotazione {refer}: {response.content}")

#     return response.content


# access_token_basic = get_access_token_basic()
# access_token_full = get_access_token_full()
# print(f"Ecco il token con grant parziale:{access_token_basic}")
# print(f"Ecco il token con grant completo:{access_token_full}")

# accommodations = fetch_accommodations(access_token_basic)

# accommodation_id = choose_accommodation(accommodations)

# reservations = fetch_reservations(access_token_full, accommodation_id)
# print(f"Ecco le prenotazioni relative a {accommodation_id}: {reservations}")

# # Nuova parte: gestire ogni prenotazione
# for reservation in reservations['data']:
#     handle_new_booking(reservation)






# def fetch_webhooks(access_token_full):
#     endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access_token_full}"
#     }

#     response = requests.get(endpoint, headers=headers)
#     print("ciaoS")
#     if response.status_code != 200:
#         print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
#         return []

#     return response.json()

# webhook_url="https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
# webhooks = fetch_webhooks(access_token_full)
# print(f"Ecco una lista di possibili webhook:{webhooks}")

# CODICE CHE MANDA CORRETTAMENTE LE PRENOTAZIONI ANCHE NUOVE AL WEBHOOK: 
# TUTTAVIA NON MI RESTITUISCE LE PRENOTAZIONI SOTTOPOSTE AD AZIONI NELLE PRENOTAZIONI DI DEFAULT RELATIVE AD UNA CERTA ACCOMODATION
from odoo import http, models, api, fields
from odoo.http import request
import requests
import json


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
        "code": "383b5de626be4b439204ca69d2849eacedc507fd743b43ee9b01fd94bc709b6f",
        "grant_type": "authorization_code",
        "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
    }
    response = requests.post(endpoint, data=payload, headers=headers)
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


def fetch_reservations(token, accommodation_id):
    endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

def handle_new_booking(booking_data):
    refer = booking_data.get('refer')
    # accommodation_id = booking_data.get("accommodation")["id"]
    accommodation_id = booking_data.get("accommodation")["id"]
    url= f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    # url = f"https://api.octorate.com/api/v1/accommodations/{accommodation_id}/bookings/"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
    new_booking_data = {"content": json.dumps({"refer": refer,})}
    response = requests.post(url, headers=headers, data=json.dumps(new_booking_data))
    return response.content

def send_to_webhook(webhook_url, reservations):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
    data = {"reservations": reservations}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    return response.content

def fetch_webhooks(access_token_full):
    endpoint = "https://api.octorate.com/connect/rest/v1/subscription"
    headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token_full}"}
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        return []
    return response.json()

access_token_basic = get_access_token_basic()
access_token_full = get_access_token_full()
print(f"Ecco il token con grant parziale:{access_token_basic}")
print(f"Ecco il token con grant completo:{access_token_full}")

accommodations = fetch_accommodations(access_token_basic)
accommodation_id = choose_accommodation(accommodations)
reservations = fetch_reservations(access_token_full, accommodation_id)
print(f"Ecco le prenotazioni relative a {accommodation_id}: {reservations}")

# 

# all_reservations = reservations['data']
all_reservations = reservations['data']
new_reservations = []  # Implementa la logica per ottenere/creare nuove prenotazioni
all_reservations.extend(new_reservations)
print(f"Ecco le prenotazioni aggiornate:{all_reservations}")

webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
send_to_webhook(webhook_url, all_reservations)
webhooks = fetch_webhooks(access_token_full)

# NEW CODE:Questo codice è stato adattato per utilizzare un singolo metodo send_http_request per gestire sia le richieste GET che POST. 
# Inoltre, è stata aggiunta una funzione di test test_fetch_reservations per dimostrare come si potrebbe testare la funzione fetch_reservations utilizzando unittest.mock. 

# from unittest import mock
# import requests
# import json

# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

# def get_access_token_basic():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     payload = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
#     response = requests.post(endpoint, data=payload, headers=headers)
#     return response.json().get("access_token", None)

# def get_access_token_full():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"
#     headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "code": "c2e80996c3e842a3a22c46fd62e98868f0218f59fbaf4d3da0a94e0e2f125dca",
#         "grant_type": "authorization_code",
#         "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
#     }
#     response = requests.post(endpoint, data=payload, headers=headers)
#     return response.json().get("access_token", None)

# def send_http_request(method, url, headers, data=None):
#     try:
#         if method == "GET":
#             response = requests.get(url, headers=headers)
#         elif method == "POST":
#             response = requests.post(url, headers=headers, data=data)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print(f"Si è verificato un errore di richiesta: {e}")
#         return None

#     if response.status_code != 200:
#         print(f"Errore nella richiesta: Status code {response.status_code}, Risposta {response.text}")
#         return None

#     if not response.content or 'application/json' not in response.headers['Content-Type']:
#         print(f"Risposta non valida o non JSON: {response.content}")
#         return None
#     if response.status_code == 204:
#         return None  # o gestiscilo in modo appropriato per la tua applicazione


#     try:
#         return response.json()
#     except json.JSONDecodeError as e:
#         print(f"Errore durante la decodifica JSON: {e}, Risposta ricevuta: {response.text}")
#         return None


# def fetch_accommodations(token):
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
#     return send_http_request("GET", endpoint, headers)

# def choose_accommodation(accommodations):
#     print("Scegli un accommodation:")
#     for index, accommodation in enumerate(accommodations, start=1):
#         print(f"{index}. {accommodation.get('name', 'Nome non disponibile')} (ID: {accommodation.get('id', 'ID non disponibile')})")
#     choice = int(input("Inserisci il numero corrispondente all'accommodation: "))
#     return accommodations[choice-1].get("id")

# def fetch_reservations(token, accommodation_id):
#     endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
#     return send_http_request("GET", endpoint, headers)

# def handle_new_booking(booking_data):
#     refer = booking_data.get('refer')
#     accommodation_id = booking_data.get("accommodation")["id"]
#     url= f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
#     new_booking_data = {"content": json.dumps({"refer": refer,})}
#     return send_http_request("POST", url, headers, json.dumps(new_booking_data))

# def send_to_webhook(webhook_url, reservations):
#     headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
#     data = {"reservations": reservations}
#     return send_http_request("POST", webhook_url, headers, json.dumps(data))

# def fetch_webhooks(access_token_full):
#     endpoint = "https://api.octorate.com/connect/rest/v1/subscription"
#     headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token_full}"}
#     return send_http_request("GET", endpoint, headers)

# access_token_basic = get_access_token_basic()
# access_token_full = get_access_token_full()
# print(f"Ecco il token con grant parziale:{access_token_basic}")
# print(f"Ecco il token con grant completo:{access_token_full}")

# accommodations = fetch_accommodations(access_token_basic)
# accommodation_id = choose_accommodation(accommodations)
# reservations = fetch_reservations(access_token_full, accommodation_id)
# print(f"Ecco le prenotazioni relative a {accommodation_id}: {reservations}")

# all_reservations = reservations['data']
# new_reservations = []
# all_reservations.extend(new_reservations)
# print(f"Ecco le prenotazioni aggiornate:{all_reservations}")

# # webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
# webhook_url = "https://webhook.site/e0cb21f2-cbfd-4365-bff9-44f455964eb8"

# send_to_webhook(webhook_url, all_reservations)
# webhooks = fetch_webhooks(access_token_full)

# def test_fetch_reservations():
#     with mock.patch('__main__.send_http_request') as mock_request:
#         mock_request.return_value = {"data": [{"reservation_id": "test123", "name": "Test Reservation"}]}
#         result = fetch_reservations("mock_token", "mock_accommodation_id")
#         assert result == {"data": [{"reservation_id": "test123", "name": "Test Reservation"}]}



# QUESTO SNIPPET FUNZIONA NELL'INVIARE I DATI DI PRENOTAZIONE AL WEBHOOK, MA NON è INTEGRATO CON ODOO
# class RoomBookingController(http.Controller):

#     @http.route('/room_booking/webhook', type='json', auth='public', methods=['POST'])
#     def receive_data(self, **kw):
#         data = request.jsonrequest
#         event_type = data.get('type')
#         webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"

#         headers = {
#             'Content-Type': 'application/json'
#         }

#         response_message = {"message": "Event not supported"}

#         if event_type == "RESERVATION_CREATED":
#             reservation = request.env['bb_booking.roombooking'].sudo().create({
#                 'refer': data.get('reservation_id'),
#                 'checkin': data.get('checkin'),
#                 'checkout': data.get('checkout'),
#                 'totalChildren': data.get('totalChildren'),
#                 'totalInfants': data.get('totalInfants'),
#                 'totalGuest': data.get('totalGuest'),
#                 'roomGross': data.get('roomGross'),
#                 'totalGross': data.get('totalGross'),
#             })

#             try:
#                 response = requests.post(webhook_url, json=data, headers=headers)
#                 if response.status_code == 200:
#                     response_message = {"message": "Reservation created and data sent to webhook"}
#                 else:
#                     response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#             except requests.RequestException as e:
#                 response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CANCELLED":
#             reservation_id = data.get('reservation_id')
#             # reservation = request.env['bb_booking.roombooking'].sudo().search([('id', '=', reservation_id)])
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 # reservation.write({'refer': 'Cancellato'})
#                 reservation.write({'status': 'Cancellato'})

#                 # Invia i dati al webhook
#                 try:
#                     response = requests.post(webhook_url, json=data, headers=headers)  # Qui includiamo gli headers
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation cancelled and data sent to webhook"}
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except requests.RequestException as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CONFIRMED":
#             reservation_id = data.get('reservation_id')
#             # reservation = request.env['bb_booking.roombooking'].sudo().search([('id', '=', reservation_id)])
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 # reservation.write({'refer': 'Confermato'})
#                 reservation.write({'status': 'Confermato'})

#                 try:
#                     response = requests.post(webhook_url, json=data, headers=headers)
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation confirmed and data sent to webhook"}
#                         print(response_message)
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except requests.RequestException as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         return response_message

# NEW ATTEMPT PER DOMANI (12/10/2023)


# class RoomBookingController(http.Controller):

#     @http.route('/reservation/webhook', type='json', auth='public', methods=['POST'])
#     def receive_data(self, **kw):
#         print("ok")
#         data = request.jsonrequest
#         event_type = data.get('type')
#         webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
#         headers = {'Content-Type': 'application/json'}
#         response_message = {"message": "Event not supported"}

#         if event_type == "RESERVATION_CREATED":
#             print("hello world")
#             reservation = request.env['bb_booking.roombooking'].sudo().create({
#                 'refer': data.get('refer'),
#                 'checkin': data.get('checkin'),
#                 'checkout': data.get('checkout'),
#                 'totalChildren': data.get('totalChildren'),
#                 'totalInfants': data.get('totalInfants'),
#                 'totalGuest': data.get('totalGuest'),
#                 'roomGross': data.get('roomGross'),
#                 'totalGross': data.get('totalGross'),
#             })

#             try:
#                 response = requests.post(webhook_url, json=data, headers=headers)
#                 if response.status_code == 200:
#                     response_message = {"message": "Reservation created and data sent to webhook"}
#                 else:
#                     response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#             except requests.RequestException as e:
#                 response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CANCELLED":
#             reservation_id = data.get('reservation_id')
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 reservation.write({'status': 'Cancellato'})

#                 try:
#                     response = requests.post(webhook_url, json=data, headers=headers)
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation cancelled and data sent to webhook"}
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except requests.RequestException as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         elif event_type == "RESERVATION_CONFIRMED":
#             reservation_id = data.get('reservation_id')
#             reservation = request.env['bb_booking.roombooking'].sudo().search([('refer', '=', reservation_id)])

#             if reservation:
#                 reservation.write({'status': 'Confermato'})

#                 try:
#                     response = requests.post(webhook_url, json=data, headers=headers)
#                     if response.status_code == 200:
#                         response_message = {"message": "Reservation confirmed and data sent to webhook"}
#                     else:
#                         response_message = {"message": f"Failed to send data to webhook: {response.status_code} - {response.text}"}
#                 except requests.RequestException as e:
#                     response_message = {"message": f"Request failed: {str(e)}"}

#         return response_message



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

