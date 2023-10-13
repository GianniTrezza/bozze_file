from odoo import http, models, fields, api
from odoo.http import request
import requests

class RoomBookingController(http.Controller):

    @http.route('/room_booking/webhook', type='json', auth='public', methods=['POST'])
    def receive_data(self, **kw):
        data = request.jsonrequest

        room_booking = request.env['bb_booking.roombooking'].sudo().create({
            'refer': data.get('refer'),
            'status': data.get('status'),
            'checkin': data.get('checkin'),
            'checkout': data.get('checkout'),
            'createTime': data.get('createTime'),
            'updateTime': data.get('updateTime'),
            'channelNotes': data.get('channelNotes'),
            'children': data.get('children'),
            'infants': data.get('infants'),
            'phone': data.get('phone'),
            'roomGross': data.get('roomGross'),
            'totalGross': data.get('totalGross'),
            'totalGuest': data.get('totalGuest'),
            'arrivalTime': data.get('arrivalTime'),
            'channelName': data.get('channelName'),
            'currency': data.get('currency'),
            'firstName': data.get('firstName'),
            'guestMailAddress': data.get('guestMailAddress'),
            'booking_id': data.get('id'),
            'lastName': data.get('lastName'),
            'paymentStatus': data.get('paymentStatus'),
            'paymentType': data.get('paymentType'),
            'product_id': data.get('product_id'),
            'roomName': data.get('roomName'),
            'rooms': data.get('rooms'),
            'totalChildren': data.get('totalChildren'),
            'totalInfants': data.get('totalInfants'),
            'totalPaid': data.get('totalPaid'),
            'touristTax': data.get('touristTax'),
        })

        api_config = request.env['solt.http.test'].sudo().search([], limit=1)
        if api_config:
            api_config.action_request(data)

        return {"message": "Data received and saved successfully"}

    @http.route('/fetch_bookings', type='json', auth='public', methods=['POST'])
    # Caso uno: assenza di fitri
    def fetch_bookings(self, **kw):
        # Assenza di filtri
        accommodations_url = "https://api.octorate.com/connect/accommodations" 
        # /rest/v1/accommodation
        accommodations_response = requests.get(accommodations_url) 
        accommodations_data = accommodations_response.json()
        
    


        bookings_url = "https://api.octorate.com/connect/reservations"
        bookings_response = requests.post(bookings_url, json={"Accomodation": accommodations_data.get('id')}) 
        bookings_data = bookings_response.json()

        api_config = request.env['solt.http.test'].sudo().search([], limit=1)
        if api_config:
            api_config.action_request_with_structure(bookings_data)

        return {"message": "Bookings fetched and processed successfully"}
    # Caso 2: Presenza di filtri a scelt
    # @http.route('/fetch_bookings', type='json', auth='public', methods=['POST'])
    def fetch_bookings(self, **kw):
        data = request.jsonrequest
        accommodation_address = data.get('content').get('accommodation').get('address')

        bookings_url = "https://api.octorate.com/connect/reservations"
        bookings_response = requests.post(bookings_url, json={"Accomodation": {"address": accommodation_address}})
        bookings_data = bookings_response.json()

        api_config = request.env['solt.http.test'].sudo().search([], limit=1)
        if api_config:
            api_config.action_request_with_structure(bookings_data)

        return {"message": "Bookings fetched successfully"}


class SoltHttpTest(models.Model):
    _name = 'solt.http.test'

    name = fields.Char('URL')
    method = fields.Selection([('post', 'POST'), ('get', 'GET'), ('put', 'PUT'), ('patch', 'PATCH'), ('delete', 'DELETE')], string='HTTP Method')
    user = fields.Char('User')
    password = fields.Char('Password')
    content = fields.Text('Content')
    response = fields.Text('Response')

    # Caso 1: Assenza di filtri: questo caso vale anche per la presenza di filtri
    @api.multi
    def action_request_with_structure(self, content_data=None):
        for test in self:
            endpoint = test.name
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            auth = (test.user, test.password) if test.user and test.password else None
            content = {"role": "system", "content": "Fetching bookings", "data": test.content if not content_data else content_data}
            result = getattr(requests, test.method)(endpoint, json=content, auth=auth, headers=headers)
            test.write({'response': result.text})

    


# OPPURE
    @api.multi
    def add_accommodation(self, accommodation_data):
        for test in self:
            endpoint = "URL_OCTORATE/rest/v1/accommodation"
            # Oppure
            endpoint = "URL_OCTORATE/rest/accommodation" 
            # Esempio di endpoint = "https://api.octorate.example.com/rest/accommodation"
            # endpoint = "https://api.octorate.com/rest/v1/accommodation" 
            headers = {
                'Content-Type': 'application/json', 
                'Authorization': 'Basic YOUR_BASE64_CREDENTIALS', # Sostituisci con le tue credenziali base64
                'key': 'YOUR_KEY' # Sostituisci con la tua chiave
            }
            
            result = requests.post(endpoint, json=accommodation_data, headers=headers)
            
            if result.status_code == 200:
                response_data = result.json()
                if response_data.get("status") == "created":
                    # Gestisci la risposta di successo, ad esempio salvando il codice della proprietà
                    pass
                else:
                    # Gestisci gli errori di validazione o altri errori relativi ai dati
                    pass
            elif result.status_code in [401, 403]:
                # Gestisci gli errori di autenticazione e autorizzazione
                pass

            test.write({'response': result.text})

            # POSSIBILE FLOWCHART PER LA CREAZIONE DELL'API INTEGRANTE OCTORATE CON ODOO
# 1) COME CREARE UN'API KEY DA DARE IN PASTO ALLA KEY DEGLI HEADERS
# PREMESSA
# Utenti della Chiave API (API attivate prima del 17-03-2020, Migrazione da Formato XML a JSON)
# Per elaborare le richieste con la nuova API, dovresti seguire il metodo precedentemente menzionato.
# Contattaci per ottenere le nuove credenziali; successivamente, potrai ottenere il token per le tue proprietà utilizzando il metodo Identity->migrateApiKey.

# CREAZIONE API KEY DA OCTORATE
# Per generare una chiave API da un servizio specifico (come Octorate, nel tuo caso), generalmente dovresti:

# a)Accedere al tuo account sul sito web o piattaforma del servizio.
# b)Navigare verso la sezione "Impostazioni", "Developers", "API", o una sezione simile, a seconda della piattaforma.
# c)Qui, dovresti trovare un'opzione per generare una nuova chiave API o visualizzare le chiavi esistenti.
# d)Segui le istruzioni fornite per ottenere la tua chiave


# A) CONTATTA IL FORNITORE:Dovresti contattare Octorate per richiedere le nuove credenziali. 
# Possono fornirti direttamente una nuova API key o darti accesso a un portale dove puoi generare tu stesso la chiave
# B) Migrazione da XML a JSON: Una volta ottenute le nuove credenziali, sembra che ci sia un metodo chiamato migrateApiKey sotto una categoria chiamata Identity che dovresti utilizzare per ottenere un token per le tue proprietà. 
# Questo potrebbe essere necessario se stavi utilizzando la vecchia API con formato XML e ora devi migrare a una nuova versione che utilizza JSON.
# C) Utilizzo della Nuova API Key: Una volta ottenuta la nuova API key o il token, dovresti utilizzarla nelle tue richieste API come valore dell'header key.
#  Assicurati di seguire le specifiche menzionate nella documentazione o nelle istruzioni fornite dal supporto di Octorate.
# D)Testa la Nuova API: È sempre una buona pratica testare la nuova API in un ambiente sicuro (come un ambiente di test o di sviluppo) prima di usarla in produzione.
#  Assicurati che tutto funzioni come previsto e che i dati vengano trasmessi nel formato corretto.


# 2) COME CREARE UN API

# A) Creazione stringa base 64 per autorizazione (esempio)

# Username: myUsername
# Password: myPassword

import base64

credentials = "myUsername:myPassword"
base64_credentials = base64.b64encode(credentials.encode()).decode()
print(base64_credentials)

# esempio di base64_credentials: bXlVc2VybmFtZTpteVBhc3N3b3Jk
# Esempio di key: abc1234defgh
# B)
# Headers model
# headers = {
#     'Authorization': 'Basic bXlVc2VybmFtZTpteVBhc3N3b3Jk', 
#     'key': 'abc1234defgh', usare come key l'api key seguente le istruzioni del punto precedente
#     'Content-Type': 'application/json'
# }

# C) Integrazione della sottostante funzione nel metodo add_accommodation(self, accommodation_data):
# import json
# import requests

# def manage_bookings(accommodation_id, new_refer):
#     headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}

#     # Recupera le prenotazioni esistenti
#     get_url = f"https://api.octorate.com/connect/rest/v1/reservations?accommodation_id={accommodation_id}"
#     get_response = requests.get(get_url, headers=headers)

#     if get_response.status_code != 200:
#         print(f"Errore nel recupero delle prenotazioni: {get_response.status_code}")
#         return None

#     bookings = get_response.json()  # adatta questa parte in base al formato della risposta dell'API

#     # Crea una nuova prenotazione
#     post_url = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     new_booking_data = {"content": json.dumps({"refer": new_refer,})}

#     post_response = requests.post(post_url, headers=headers, data=json.dumps(new_booking_data))

#     if post_response.status_code == 200:  # o un altro codice appropriato per il tuo caso
#         new_booking = post_response.json()  # adatta questa parte in base al formato della risposta dell'API
#         bookings.append(new_booking)
#     else:
#         print(f"Errore durante la creazione della nuova prenotazione: {post_response.status_code}")

#     return bookings

# # Esempio di utilizzo:
# accommodation_id, new_refer = choose_accommodation()  # questa funzione restituisce l'ID dell'alloggio e il refer
# updated_bookings = manage_bookings(accommodation_id, new_refer)








