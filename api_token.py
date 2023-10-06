# # import requests



# # # Endpoint per ottenere il token
# # TOKEN_URL = "https://api.octorate.com/connect/rest/v1/identity/apilogin"

# # # Credenziali della tua applicazione (queste vanno ottenute da Octorate)
# # CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"  # Sostituisci con il tuo client_id
# # CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"  # Sostituisci con il tuo client_secret

# # # Dati del corpo della richiesta
# # payload = {
# #     "grant_type": "client_credentials",
# #     "client_id": CLIENT_ID,
# #     "client_secret": CLIENT_SECRET
# # }

# # # print(payload)

# # # Eseguire la richiesta POST per ottenere il token
# # response = requests.post(TOKEN_URL, data=payload)
# # print(response.json())

# # token_data = response.json()
# # # print(token_data)

# # # Estrarre il token di accesso dalla risposta
# # access_token = token_data.get("access_token")

# # print(access_token)

# # # Adesso puoi utilizzare questo token di accesso per fare richieste alle API di Octorate
# # VECCHIO CODICE
# import requests
# import base64
# import json

# def get_access_token():
#     TOKEN_URL = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
#     CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
#     CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"
    
#     payload = {
#         "grant_type": "client_credentials",
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET
#     }
    
#     response = requests.post(TOKEN_URL, data=payload)
#     token_data = response.json()
#     return token_data.get("access_token")
# new_token= get_access_token()
# print(new_token)

# def create_accommodation(access_token, accommodation_data):
#     # ACCESSO A WEBHOOK
#     #endpoint = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd/rest/accommodation"
#     # Vecchio attempt di accesso
#     # endpoint = "https://admin.octorate.com/octobook/rest/accommodation"
#     # NEW attempt di accesso ad Octorate
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation'"
    

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}",
#     }
    
#     response = requests.post(endpoint, json=accommodation_data, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore: {response.status_code} - {response.text}")
#         return None

#     try:
#         data = response.json()
#         return data.get('codice')
#     except json.decoder.JSONDecodeError:
#         print("Errore nella decodifica del JSON. Risposta ricevuta:", response.text)
#         return None
#     # data = response.json()
#     # return data.get('codice')

# def fetch_reservations(access_token, accommodation_id):
#     # ACCESSO A WEBHOOK
#     # endpoint = f"https://admin.octorate.com/octobook/connect/reservations?accommodation_id={accommodation_id}"
#     # endpoint = f"https://webhook.site/#!/e2e61afa-8888-487d-a8d6-4c79156487dd/e7bf429b-2e66-46ac-b0d0-542f3b7ea241/1/connect/reservations?accommodation_id={accommodation_id}"
#     # New accesso ad Octorate
#     endpoint= f"https://api.octorate.com/connect/rest/v1/reservation?accommodation_id={accommodation_id}"

    
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     response = requests.get(endpoint, headers=headers)
#     # Verifica lo stato della risposta
#     if response.status_code != 200:
#         print(f"Errore: {response.status_code} - {response.text}")
#         return []

#     try:
#         return response.json()
#     except json.decoder.JSONDecodeError:
#         print("Errore nella decodifica del JSON. Risposta ricevuta:", response.text)
#         return []

# # def transform_reservations(original_reservations):
# #     transformed = []
    
# #     for data in original_reservations:
# #         transformed.append({
# #             'status': data.get('status'),
# #             'checkin': data.get('checkin'),
# #             'checkout': data.get('checkout'),
# #         })
    
# #     return transformed

# if __name__ == "__main__":
#     credentials = "api_test_odooerp:verNqvvXD"
#     base64_credentials = base64.b64encode(credentials.encode()).decode()

#     access_token = get_access_token()
#     accommodation_data = {
#         "address": "via filippo caruso",
#         "city":"ROMA",   
#     }
#     # lastName': data.get('lastName')
    
#     accommodation_id = create_accommodation(access_token, accommodation_data)
#     original_reservations = fetch_reservations(access_token, accommodation_id)
    
#     # transformed_reservations = transform_reservations(original_reservations)
    
#     print(f"Le prenotazioni ricevute sono", original_reservations)

# NEW CODE
import requests
import json

# Funzione per ottenere il token di accesso
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

# Funzione per ottenere gli accomodations
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

def choose_accommodation(accommodations):
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
        print(f"Errore: {response.status_code} - {response.text}")
        return []
    
    return response.json()

# Funzione per vedere i webhooks attualmente configurati
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

# Funzione per aggiungere un webhook
def add_webhook(access_token, event, url_webhook):
    endpoint = f"https://api.octorate.com/connect/rest/v1/subscription/{event}"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }
    
    payload = {
        "url": url_webhook
    }
    
    response = requests.post(endpoint, data=payload, headers=headers)
    if response.status_code != 200:
        print(f"Errore: {response.status_code} - {response.text}")
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
accommodation_id = choose_accommodation(accommodations)
print(f"Hai scelto l'accomodation con ID: {accommodation_id}")

# try:
#     reservations = fetch_reservations(token, accommodation_id)
#     print(f"Prenotazioni per l'alloggio {accommodation_id}: {reservations}")
#     webhooks = fetch_webhooks(token)
#     print(f"Webhooks attualmente configurati: {webhooks}")
# except ApiSecurityException as e:
#     print(f"Errore nel recupero dei dati: {e.message}")



reservations = fetch_reservations(token, accommodation_id)
print(f"Reservations per l'accomodation {accommodation_id}: {reservations}")
webhooks = fetch_webhooks(token)
print(f"Webhooks attualmente configurati: {webhooks}")

evento = choose_event()
url_webhook = "https://webhook.site"
response = add_webhook(token, evento, url_webhook)
print(f"Risposta dall'aggiunta del webhook: {response}")






