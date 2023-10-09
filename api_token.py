# NEW ATTEMPT (9 OTTOBRE)
import requests

def get_access_token():
    TOKEN_URL = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
    CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
    CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"
    
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    token_data = response.json()
    return token_data.get("access_token")

def fetch_accommodations(access_token):
    endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore: {response.status_code} - {response.text}")
        return []
    return response.json()
# ASSENZA DI FILTRI
# def choose_accommodation(accommodations):
#     print("Scegli un accommodation:")
#     for index, accommodation in enumerate(accommodations, start=1):
#         print(f"{index}. {accommodation.get('name', 'Nome non disponibile')} (ID: {accommodation.get('id', 'ID non disponibile')})")
#     choice = int(input("Inserisci il numero corrispondente all'accommodation: "))
#     return accommodations[choice-1].get("id")

# PRESENZA FILTRI
# Funzione per scegliere l'accomodation
def choose_accommodation(accommodations):
    print("Vuoi filtrare gli accommodations per indirizzo? [S/n]")
    choice = input().lower()
    if choice == 's':
        address_filter = input("Inserisci l'indirizzo dell'accommodation: ")
        filtered_accommodations = [a for a in accommodations if address_filter.lower() in a.get('address', '').lower()]
        if not filtered_accommodations:
            print("Nessun accommodation trovato con quell'indirizzo.")
            return None
        accommodations = filtered_accommodations

    print("Scegli un accommodation:")
    for index, accommodation in enumerate(accommodations, start=1):
        print(f"{index}. {accommodation.get('name', 'Nome non disponibile')} (ID: {accommodation.get('id', 'ID non disponibile')})")
    choice = int(input("Inserisci il numero corrispondente all'accommodation: "))
    return accommodations[choice-1].get("id")

# Funzione per ottenere le reservations per un determinato accomodation
def fetch_reservations(access_token, accommodation_id):
    endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore nel recupero delle prenotazioni: {response.status_code} - {response.text}")
        return []
    return response.json()

def fetch_webhooks(access_token):
    endpoint = "https://api.octorate.com/connect/rest/v1/subscription"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore: {response.status_code} - {response.text}")
        return []
    return response.json()

def add_webhook(access_token, event, url_webhook):
    endpoint = f"https://api.octorate.com/connect/rest/v1/subscription/{event}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }
    
    payload = {
        "url": url_webhook
    }
    
    response = requests.post(endpoint, data=payload, headers=headers)
    if response.status_code != 200:
        print(f"Errore nell'aggiunta del webhook: {response.status_code} - {response.text}")
        return None
    return response.json()

EVENTS = [
    "RESERVATION_CREATED",
    "RESERVATION_CHANGE",
    "RESERVATION_CANCELLED",
    "RESERVATION_CONFIRMED",
    "CONTENT_NOTIFICATION",
    "CONTENT_PUSH",
    "PORTAL_SUBSCRIPTION_CALENDAR",
    "XXX_NOT_USED_PORTAL_PROCESS_FAILED",
    "CHAT_MESSAGE_RECEIVED"
]

def choose_event():
    print("Scegli un evento per configurare il webhook:")
    for index, event in enumerate(EVENTS, start=1):
        print(f"{index}. {event}")
    choice = int(input("Inserisci il numero corrispondente all'evento: "))
    return EVENTS[choice-1]

token = get_access_token()
print(f"Token ottenuto: {token}")
accommodations = fetch_accommodations(token)
print(f"Accommodations ottenuti: {accommodations}")
if accommodations:
    # 1) Selezione automatica dell'accommodation (sistemazione)
    accommodation_id= accommodations[0].get("id")
    # 2) oppure, scelta dell'accommodation
    # accommodation_id = choose_accommodation(accommodations)
    print(f"Hai scelto l'accomodation con ID: {accommodation_id}")
    # La reservation è la prenotazione da scegliersi in relazione all'accomodation
    reservations = fetch_reservations(token, accommodation_id)
    print(f"Reservations per l'accomodation {accommodation_id}: {reservations}")
    webhooks = fetch_webhooks(token)
    print(f"Webhooks attualmente configurati: {webhooks}")
    # Scelta evento
    evento = choose_event()
    url_webhook = "https://webhook.site/https://webhook.site/#!/e2e61afa-8888-487d-a8d6-4c79156487dd"
    response = add_webhook(token, evento, url_webhook)
    print(f"Risposta dall'aggiunta del webhook: {response}")
else:
    print("Nessun accomodation disponibile")

# FUNZIONE SIMONE

# # URL corretto per il webhook
# url_webhook = "https://webhook.site/https://webhook.site/#!/e2e61afa-8888-487d-a8d6-4c79156487dd"
# token = get_access_token()
# print(f"Token ottenuto: {token}")
# accommodations = fetch_accommodations(token)
# # Utilizziamo il primo accomodation automaticamente
# if accommodations:
#   accommodation_id = accommodations[0].get("id")
#   print(f"Ho scelto automaticamente l'accomodation con ID: {accommodation_id}")
#   reservations = fetch_reservations(token, accommodation_id)
#   print(f"Reservations per l'accomodation {accommodation_id}: {reservations}")
#   webhooks = fetch_webhooks(token)
#   print(f"Webhooks attualmente configurati: {webhooks}")
#   # Sostituisci 'EVENT' con l'evento desiderato
#   EVENT = "RESERVATION_CREATED"
#   response = add_webhook(token, EVENT, url_webhook)
#   print(f"Risposta dall'aggiunta del webhook: {response}")
# else:
#   print("Nessun accomodation disponibile.")
