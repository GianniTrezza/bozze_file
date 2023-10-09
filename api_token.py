# NEW ATTEMPT (9 OTTOBRE)
# 1. CODICE RIADATTATO

import requests

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
    if response.status_code != 200:
        print(f"Errore: {response.status_code} - {response.text}")
        return None

    return response.json()["access_token"]

# Funzione per ottenere gli accomodations con il token di accesso
def fetch_accommodations(token):
    endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore: {response.status_code} - {response.text}")
        return []

    return response.json()
def choose_accommodation(accommodations):
    # print("Vuoi filtrare gli accommodations per indirizzo? [S/n]")
    # choice = input().lower()
    # if choice == 's':
    #     address_filter = input("Inserisci l'indirizzo dell'accommodation: ")
    #     filtered_accommodations = [a for a in accommodations if address_filter.lower() in a.get('address', '').lower()]
    #     if not filtered_accommodations:
    #         print("Nessun accommodation trovato con quell'indirizzo.")
    #         return None
    #     accommodations = filtered_accommodations

    print("Scegli un accommodation:")
    for index, accommodation in enumerate(accommodations, start=1):
        print(f"{index}. {accommodation.get('name', 'Nome non disponibile')} (ID: {accommodation.get('id', 'ID non disponibile')})")
    choice = int(input("Inserisci il numero corrispondente all'accommodation: "))
    return accommodations[choice-1].get("id")

# # Funzione per ottenere le reservations per un determinato accomodation con il token di accesso
def fetch_reservations(token, accommodation_id):
    endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore: {response.status_code} - {response.text}")
        return []

    return response.json()

# Ottieni il token di accesso
access_token = get_access_token()
if access_token:
    print(f"Token di accesso ottenuto con successo: {access_token}")

# Esempio: Ottenere gli accomodations
accommodations = fetch_accommodations(access_token)
if accommodations:
        # 1) Selezione automatica dell'accommodation (sistemazione)
    # accommodation_id= accommodations[0].get("id")
    # 2) oppure, scelta dell'accommodation
    accommodation_id = choose_accommodation(accommodations)
    print(f"Hai scelto l'accomodation con ID: {accommodation_id}")

        # Esempio: Ottenere le reservations per l'accomodation selezionata
    reservations = fetch_reservations(access_token, accommodation_id)
    print(f"Reservations per l'accomodation {accommodation_id}: {reservations}")
    
else:
    print("Nessun accomodation disponibile.")



def fetch_webhooks():
    endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore: {response.status_code} - {response.text}")
        return []

    return response.json()


webhooks = fetch_webhooks()
print(f"Webhooks configurati: {webhooks}")



def choose_event():
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
    while True:
        print("Scegli un evento per configurare il webhook:")
        for index, event in enumerate(EVENTS, start=1):
            print(f"{index}. {event}")
        try:
            choice = int(input("Inserisci il numero corrispondente all'evento: "))
            if 1 <= choice <= len(EVENTS):
                return EVENTS[choice-1]
            else:
                print(f"Errore: seleziona un numero tra 1 e {len(EVENTS)}")
        except ValueError:
            print("Errore: inserisci un numero valido.")


def add_webhook(event, url_webhook):
    endpoint = f"https://api.octorate.com/connect/rest/v1/subscription/{event}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "url": url_webhook
    }

    response = requests.post(endpoint, data=payload, headers=headers)
    if response.status_code != 200:
        print(f"Errore nell'aggiunta del webhook: {response.status_code} - {response.text}")
        return False

    print(f"Webhook configurato con successo per l'evento {event}.")
    return True


# Specifica l'evento e l'URL del webhook che desideri aggiungere
event_to_add = choose_event()
url_to_add = "https://webhook.site/#!/e2e61afa-8888-487d-a8d6-4c79156487dd"

if add_webhook(event_to_add, url_to_add):
    print(f"Webhook aggiunto con successo per l'evento {event_to_add}.")
else:
    print(f"Errore nell'aggiunta del webhook per l'evento {event_to_add}.")


# 1.1 OUTPUT (CON ERRORI RELATIVI PRESENTI) RELATIVI AL CODICE PRECEDENTE PER QUANTO IL FLUSSO SIA CORRETTO:
# A)Errore nel recupero delle prenotazioni: 403 - {"message":"errNoResourcesForIdentity","nested":[],"type":"ApiSecurityException"}
# Reservations per l'accomodation 557782: []
# B) Scegli un evento per configurare il webhook:
# 1. RESERVATION_CREATED
# 2. RESERVATION_CHANGE
# 3. RESERVATION_CANCELLED
# 4. RESERVATION_CONFIRMED
# 5. CONTENT_NOTIFICATION
# 6. CONTENT_PUSH
# 7. PORTAL_SUBSCRIPTION_CALENDAR
# 8. XXX_NOT_USED_PORTAL_PROCESS_FAILED
# 9. CHAT_MESSAGE_RECEIVED
# Inserisci il numero corrispondente all'evento: 2
# Errore nell'aggiunta del webhook: 400 - {"element":"Prevalidation of Content","message":" Even though the call is technically correct, the content registered inside the system cannot be validated agaist the criteria","nested":[{"human_name":"Typology","machine_name":"type","message":"Typology: Validation Error: Length is greater than allowable maximum of '1' (You have submitted: 2)","type":"RejectLenght"}],"type":"ApiValidationFailed"}
# Risposta dall'aggiunta del webhook: None

# 1.2 MODELLO DI RISPOSTA CORRETTA RELATIVO ALL'EVENTO 9 (CHAT_MESSAGGE_RECEIVED):
# Inserisci il numero corrispondente all'evento: 9
# {'url': 'https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd'}
# Risposta dall'aggiunta del webhook: {'apiMember': 578, 'createTime': '2023-10-09T10:32:18.36Z[UTC]', 'enabled': True, 
# 'endpoint': 'https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd', 'id': 1281, 'priority': 1, 'type': 'CHAT_MESSAGE_RECEIVED'}


# 2. POSSIBILI SOLUZIONI
# 2.1 COME GENERARE UN ACCESS TOKEN CON TUTTI I GRANT PARTENDO DALL'https di sotto
# # https://admin.octorate.com/octobook/identity/oauth.xhtml?client_id=aaaaaaaaaaaaaaaaaaaaaaaaaa&redirect_uri=https%3A%2F%2Fwww.mycompany.com%2Foauth_end.html&state=something_crypted


# import requests

# # Credenziali client registrate in Octorate
# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

# # URL di autorizzazione di Octorate
# AUTHORIZATION_URL = "https://admin.octorate.com/octobook/identity/oauth.xhtml"
# REDIRECT_URI = "IlTuoURIDiReindirizzamento"

# # Step 1: Redirigi l'utente all'URL di autorizzazione
# def authorize_user():
#     authorization_params = {
#         "client_id": CLIENT_ID,
#         "redirect_uri": REDIRECT_URI,
#         "response_type": "code",
#         "scope": "OAuthLogin",  # Aggiungi gli scope necessari
#     }

#     auth_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(authorization_params)}"
#     print(f"Redirigi l'utente all'URL di autorizzazione:\n{auth_url}")

# # Step 2: Scambia il codice di autorizzazione con un token di accesso
# def exchange_code_for_token(authorization_code):
#     TOKEN_URL = "https://api.octorate.com/connect/rest/v1/identity/token"

#     token_data = {
#         "grant_type": "authorization_code",
#         "code": authorization_code,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#     }

#     response = requests.post(TOKEN_URL, data=token_data)

#     if response.status_code == 200:
#         token_info = response.json()
#         access_token = token_info.get("access_token")
#         print(f"Token di accesso ottenuto:\n{access_token}")
#         return access_token
#     else:
#         print(f"Errore nello scambio del codice di autorizzazione con il token: {response.status_code} - {response.text}")
#         return None

# # Chiamate le funzioni per autorizzare l'utente e ottenere il token
# authorize_user()
# authorization_code = input("Inserisci il codice di autorizzazione: ")
# access_token = exchange_code_for_token(authorization_code)

# # Step 3: Utilizza il token di accesso per effettuare richieste API
# if access_token:
#     # Ora puoi utilizzare access_token nelle tue richieste API
#     # Esempio: Ottenere gli accomodations
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }

#     response = requests.get(endpoint, headers=headers)
#     if response.status_code == 200:
#         accommodations = response.json()
#         print(f"Accommodations:\n{accommodations}")
#     else:
#         print(f"Errore nell'ottenere gli accomodations: {response.status_code} - {response.text}")
# else:
#     print("Token di accesso non valido.")


# 3. CODICE ORIGINARIO (SIMONE): dà anch'esso i due medesimi errori (403 legato all'ApiSecurityLogin e 400 legato all'ApiValidationFailed)
# import requests

# # Dati del client per ottenere il token
# CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
# CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

# # Funzione per ottenere il token di accesso
# def get_access_token():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"

#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET
#     }

#     response = requests.post(endpoint, data=payload, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore: {response.status_code} - {response.text}")
#         return None

#     return response.json()["access_token"]

# # Funzione per ottenere gli accomodations con il token di accesso
# def fetch_accommodations(token):
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"

#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {token}"
#     }

#     response = requests.get(endpoint, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore: {response.status_code} - {response.text}")
#         return []

#     return response.json()

# # Funzione per ottenere le reservations per un determinato accomodation con il token di accesso
# def fetch_reservations(token, accommodation_id):
#     endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"

#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {token}"
#     }

#     response = requests.get(endpoint, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore: {response.status_code} - {response.text}")
#         return []

#     return response.json()

# # Ottieni il token di accesso
# access_token = get_access_token()
# if access_token:
#     print(f"Token di accesso ottenuto con successo: {access_token}")

#     # Esempio: Ottenere gli accomodations
#     accommodations = fetch_accommodations(access_token)
#     if accommodations:
#         accommodation_id = accommodations[0].get("id")
#         print(f"Ho scelto automaticamente l'accomodation con ID: {accommodation_id}")

#         # Esempio: Ottenere le reservations per l'accomodation selezionata
#         reservations = fetch_reservations(access_token, accommodation_id)
#         print(f"Reservations per l'accomodation {accommodation_id}: {reservations}")
#     else:
#         print("Nessun accomodation disponibile.")
# else:
#     print("Errore nell'ottenere il token di accesso.")


# def fetch_webhooks():
#     endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }

#     response = requests.get(endpoint, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore: {response.status_code} - {response.text}")
#         return []

#     return response.json()


# webhooks = fetch_webhooks()
# print(f"Webhooks configurati: {webhooks}")


# def add_webhook(event, url_webhook):
#     endpoint = f"https://api.octorate.com/connect/rest/v1/subscription/{event}"

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Authorization": f"Bearer {access_token}"
#     }

#     payload = {
#         "url": url_webhook
#     }

#     response = requests.post(endpoint, data=payload, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore nell'aggiunta del webhook: {response.status_code} - {response.text}")
#         return False

#     print(f"Webhook configurato con successo per l'evento {event}.")
#     return True


# # Specifica l'evento e l'URL del webhook che desideri aggiungere
# event_to_add = "RESERVATION_CREATED"
# url_to_add = "https://webhook.site/#!/e2e61afa-8888-487d-a8d6-4c79156487dd"

# if add_webhook(event_to_add, url_to_add):
#     print(f"Webhook aggiunto con successo per l'evento {event_to_add}.")
# else:
#     print(f"Errore nell'aggiunta del webhook per l'evento {event_to_add}.")
