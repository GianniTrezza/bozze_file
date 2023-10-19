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
        "code": "1762fbc182314ccd83ab0ecd3fc9453c47c26b98448b41cfba1ea38bd5b3671e",
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