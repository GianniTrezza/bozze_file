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
        "code": "4a3295fa5cca4ac19c68c831cff66758181a723114f24a5d82fb2bdf03dbecbb",
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
# SENZA FILTRI
def fetch_reservations(token, accommodation_id):
    endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

# CON FILTRI
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
url_to_add = "https://webhook.site/#!/e2e61afa-8888-487d-a8d6-4c79156487dd"

# Invia i dati al webhook
for webhook_data in webhooks:
    response = requests.post(webhook_url, json=webhook_data)
    if response.status_code == 200:
        print(f"Dati inviati con successo al webhook: {webhook_url}")
    else:
        print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")
 

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


