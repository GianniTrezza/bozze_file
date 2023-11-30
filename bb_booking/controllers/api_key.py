import requests
import json
import os


from datetime import datetime, timedelta

# Chiave segreta (ideale in una variabile d'ambiente)
secret_key = 'ff383914fe26d613ace3f52e7da13a670ee69a84'

# Payload con scadenza
payload = {
    'user_id': 3,
    'username': 'admin@admin.it',
    'ruolo': 'amministratore',
    'exp': datetime.utcnow() + timedelta(days=1)  # Token scade dopo 1 giorno
}

# Genera il token JWT
# token = jwt.encode(payload, secret_key, algorithm='HS256')
# print(token)


#Dati del client per ottenere il token
CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"

#
# # Funzione per ottenere il token di accesso
# def get_access_token():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"
#
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#
#     payload = {
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET
#     }
#
#     response = requests.post(endpoint, data=payload, headers=headers)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None
#
#
# # Ottieni il token di accesso
# access_token = get_access_token()
# if access_token:
#     print(f"Token di accesso ottenuto con successo: {access_token}")
# else:
#     print("Errore nell'ottenere il token di accesso.")
#
#
# def get_access_token2():
#     endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"
#
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#
#     payload = {
#         "grant_type": "authorization_code",
#         "code": "3c7611558345463bb4f29455cccb99f54f9a179690584decb36987c167e29886",
#         "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#         "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
#         "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
#     }
#
#     response = requests.post(endpoint, data=payload, headers=headers)
#
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#         return None
#
#
# # Ottieni il token di accesso
# access_token_a = get_access_token2()
#
# if access_token_a:
#     print(f"Token per visionare le reservation è : {access_token_a}")
# else:
#     print("Errore nell'ottenere il token di accesso.")
#
#
# def refresh_token():
#    endpoint = "https://api.octorate.com/connect/rest/v1/identity/refresh"
#
#    headers = {
#        "Accept": "application/json",
#        "Content-Type": "application/x-www-form-urlencoded"
#    }
#
#    payload = {
#                 "grant_type": "authorization_code",
#                 "code": "cc4a0b29064f4b36992e1203acdbf613eb0eda5cd36c43bab2c687820d4c8e79",
#                 "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#                 "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
#                 "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html",
#                 'refresh_token': '2acf003360ea4ebca6871b5d7e56efe2'
#    }
#
#    response = requests.post(endpoint, data=payload, headers=headers)
#
#    if response.status_code == 200:
#        print("refresh avvenuto con successo")
#        return response.json().get("access_token")
#    else:
#        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#        return None
#
#
# def fetch_accommodations(token):
#     endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
#     # print(token)
#
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {token}"
#     }
#
#     response = requests.get(endpoint, headers=headers)
#
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Errore nell'ottenere gli accommodation: {response.headers}, {headers}")
#         return []

#
# # Esempio di utilizzo:
# # Ottieni il token di accesso (già ottenuto precedentemente)
# access_token = get_access_token()
# # Ottenere gli accommodation
# accommodations = fetch_accommodations(access_token)
# if accommodations:
#     print(f"Gli accommodation ottenuti con successo: {accommodations}")
# else:
#     print("Nessun accommodation disponibile o errore nell'ottenimento.")
#
#
# def fetch_reservations_for_accommodation_id(access_token_a, accommodation_id):
#     reservation_endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {access_token_a}"
#     }
#     response = requests.get(reservation_endpoint, headers=headers)
#
#     if response.status_code == 200:
#         reservations = response.json()
#         return reservations
#     else:
#         print(
#             f"Errore nell'ottenere le prime prenotazioni per l'alloggio {accommodation_id}, {headers}, {response.status_code}, {response.text}")
#         return []
#
#
# # Esempio di utilizzo:
# # Ottieni il token di accesso (già ottenuto precedentemente)
#
# # access_token_a = get_access_token2()
# # print(access_token_a)
# # Inserisci l'ID dell'alloggio per cui desideri ottenere le prenotazioni
# accommodation_id = "632966"
#
# # Ottieni le prenotazioni per l'alloggio selezionato utilizzando il token ottenuto
# reservations = fetch_reservations_for_accommodation_id(access_token_a, accommodation_id)
#
# # Controlla se ci sono prenotazioni
# if reservations:
#     print(f"{accommodation_id}: {reservations}")
#
#     # Converti le prenotazioni in formato JSON
#     reservations_json = json.dumps(reservations)
#
#     # Definisci l'URL del webhook al quale inviare le prenotazioni
#     webhook_url = "https://webhook.site/e2e61afa-8888-487d-a8d6-4c79156487dd"
#
#     # Invia i dati al webhook
#     headers = {
#         "Content-Type": "application/json"
#     }
#
#     response = requests.post(webhook_url, data=reservations_json, headers=headers)
#
#     # Verifica la risposta del webhook
#     if response.status_code == 200:
#         print("Dati inviati con successo al webhook.")
#     else:
#         print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")
# else:
#     print("Nessuna prenotazione disponibile o errore nell'ottenimento.")
#
# print(f"{accommodation_id}:{reservations}")
#
#
#
# def fetch_webhooks(access_token_a):
#     endpoint = "https://api.octorate.com/connect/rest/v1/subscription"
#
#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access_token_a}"
#     }
#
#     response = requests.get(endpoint, headers=headers)
#     if response.status_code != 200:
#         print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
#         return []
#
#     return response.json()



#
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
       
# All'interno della funzione handle_custom_endpoint

# ...

# if tipo == 'RESERVATION_CREATED':
#     # Ricerca del contatto esistente prima di crearne uno nuovo
#     existing_contact = request.env['res.partner'].sudo().search([('email', '=', email_)], limit=1)
#     if existing_contact:
#         # Aggiornare il contatto esistente
#         existing_contact.write({
#             'name': guestsList_,
#             'street': address_,
#             'city': city_,
#             'phone': phone_
#         })
#         contact_id = existing_contact.id
#     else:
#         # Creazione di un nuovo contatto
#         contact_bb = request.env['res.partner'].sudo().create({
#             'company_type': 'person',
#             'name': guestsList_,
#             'street': address_,
#             'city': city_,
#             'email': email_,
#             'phone': phone_
#         })
#         contact_id = contact_bb.id

#     # Codice per la creazione della fattura e altre operazioni per una nuova prenotazione
#     # ...

# elif tipo == 'RESERVATION_CHANGE':
#     # Cerca la fattura esistente con il riferimento fornito
#     existing_invoice = request.env['account.move'].sudo().search([
#         ('refer', '=', refer_),
#         ('move_type', '=', 'out_invoice')
#     ], limit=1)

#     if existing_invoice:
#         # Aggiornamento della fattura esistente
#         existing_invoice.write({
#             # Aggiornamenti ai dettagli della fattura
#             # ...
#         })

#         # Aggiornamento del nome del cliente se cambiato
#         existing_contact = request.env['res.partner'].sudo().search([('id', '=', existing_invoice.partner_id.id)], limit=1)
#         if existing_contact and existing_contact.name != guestsList_:
#             existing_contact.write({'name': guestsList_})

#         # Aggiornamento delle linee di fattura
#         # ...

#     # Altri codici specifici per la gestione dei cambiamenti di prenotazione
#     # ...

# elif tipo == 'RESERVATION_CANCELLED':
#     # Gestione delle cancellazioni delle prenotazioni
#     # Trova la fattura corrispondente e aggiorna lo stato o esegui le azioni necessarie
#     # ...

# # Gestione di altri tipi di richieste o situazioni di errore
# @http.route('/api/import', cors='*', auth='public', methods=['GET'], csrf=False, website=False)
# def importazione(self, refresh_token=None, **post):
#     # ... codice precedente ...

#     fatture_per_cliente = {}  # Dizionario per tenere traccia delle fatture per ogni cliente

#     for reservation in data.get("data", []):
#         # ... estrazione dati dalla prenotazione ...
#         email_cliente = email  # Supponiamo che l'email identifichi univocamente il cliente

#         # Verifica se il cliente ha già una fattura in sospeso
#         if email_cliente not in fatture_per_cliente:
#             existing_contact = request.env['res.partner'].sudo().search([('email', '=', email_cliente)], limit=1)
#             if not existing_contact:
#                 # Crea un nuovo contatto se non esiste
#                 contact_bb = request.env['res.partner'].sudo().create({
#                     # ... dettagli del contatto ...
#                 })
#                 contact_id = contact_bb.id
#             else:
#                 contact_id = existing_contact.id

#             # Crea una nuova fattura per questo cliente
#             room_booking_obj = request.env['account.move'].sudo().create({
#                 'partner_id': contact_id,
#                 'state': 'draft',
#                 'journal_id': customer_invoice_journal.id,
#                 # ... altri dettagli della fattura ...
#             })
#             fatture_per_cliente[email_cliente] = room_booking_obj
#         else:
#             room_booking_obj = fatture_per_cliente[email_cliente]

#         # Aggiungi una linea fattura per questa prenotazione
#         request.env['account.move.line'].sudo().create({
#             'move_id': room_booking_obj.id,
#             # ... dettagli della linea fattura ...
#         })

#     # Posta tutte le fatture create
#     for room_booking_obj in fatture_per_cliente.values():
#         room_booking_obj.with_context(default_type='out_invoice').write({'state': 'draft'})
#         room_booking_obj.action_post()

#     return Response(json.dumps(response_data_list), content_type='application/json', status=200)
# ... [precedente codice per ottenere dati dalle prenotazioni] ...
# ... [precedente codice per ottenere dati dalle prenotazioni] ...

# ... [precedente codice per ottenere dati dalle prenotazioni] ...
# DOPO 
# fatture_per_cliente = {}  # Dizionario per tenere traccia delle fatture per ogni cliente

# for reservation in data.get("data", []):
#     # ... [estrazione dei dati dalla prenotazione] ...

#     email_cliente = reservation.get("email")  # Identificatore unico del cliente

#     # Ottieni o crea un contatto per il cliente
#     existing_contact = request.env['res.partner'].sudo().search([('email', '=', email_cliente)], limit=1)
#     if not existing_contact:
#         contact = request.env['res.partner'].sudo().create({
#             # ... dettagli del contatto ...
#         })
#         contact_id = contact.id
#     else:
#         contact_id = existing_contact.id

#     # Ottieni o crea una fattura per il cliente
#     if email_cliente not in fatture_per_cliente:
#         fattura = request.env['account.move'].sudo().create({
#             'partner_id': contact_id,
#             'state': 'draft',
#             'journal_id': customer_invoice_journal.id,
#             'invoice_date': fields.Date.context_today(self),
#         })
#         fatture_per_cliente[email_cliente] = fattura
#     else:
#         fattura = fatture_per_cliente[email_cliente]

#     # Crea una linea fattura per la prenotazione
#     fattura.write({
#         'invoice_line_ids': [(0, 0, {
#             'product_id': room_product.id,
#             'name': f"Prenotazione {reservation.get('riferimento')}",
#             'quantity': 1,
#             'price_unit': reservation.get("costo totale"),
#             'account_id': account_id,
#         })]
#     })

# # Finalizza le fatture
# for fattura in fatture_per_cliente.values():
#     if not fattura.invoice_line_ids:
#         _logger.error(f'Nessuna linea fattura trovata per la fattura {fattura.name}')
#         continue
#     fattura.action_post()

# # Resto del codice...

# ... [Codice precedente]
# existing_contact = request.env['res.partner'].sudo().search([('id', '=', existing_invoice.partner_id.id)], limit=1)

#         if existing_contact:
#             previous_name = existing_contact.name
#             new_name = guestsList_

#             update_vals = {}
#             name_changed = False
#             if previous_name != new_name:
#                 update_vals['name'] = new_name
#                 name_changed = True

#             if phone_ and existing_contact.phone != phone_:
#                 update_vals['phone'] = phone_

#             if update_vals:
#                 existing_contact.write(update_vals)

#             if name_changed:
#                 # Posta un messaggio nel chatter per riflettere il cambiamento del nome
#                 update_message = f"{previous_name} > {new_name} (Partner)"
#                 existing_invoice.message_post(body=update_message, message_type='comment')

#         # ... [Codice per aggiornare le linee di fattura]

#     room_booking_obj = existing_invoice

# # ... [Codice per RESERVATION_CANCELLED]

# print("La fattura ha il seguente id ---------->", room_booking_obj.id)
# if existing_contact:
#                 # ... Il tuo codice esistente per gestire il cambiamento di nome
#             else:
#                 print("Nessun contatto trovato con l'ID fornito.")
#         else:
#             print("Nessun partner associato alla fattura.")
#     else:
#         print("Nessuna fattura trovata con il riferimento fornito.")