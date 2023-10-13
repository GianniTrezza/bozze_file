# import xmlrpc.client

# url = <insert server URL>
# db = <insert database name>
# username = 'admin'
# password = <insert password for your admin user (default: admin)>
  
# http://localhost:8069/
# from odoo import http, models, fields, api
# from odoo.http import request
# import requests
# import json
# import logging
# PRIMO ATTEMPT
from odoo import http, models, fields, api
from odoo.http import request
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class SoltHttpTest(models.Model):
    _name = 'solt.http.test'
    _description = 'HTTP Test Configuration'

    name = fields.Char('URL')
    method = fields.Selection([('post', 'POST'), ('get', 'GET'), ('put', 'PUT'), ('patch', 'PATCH'), ('delete', 'DELETE')], string='HTTP Method')
    user = fields.Char('User')
    password = fields.Char('Password')
    content = fields.Text('Content')
    response = fields.Text('Response')

    # @api.multi
    def action_request_with_structure(self, content_data=None):
        self.ensure_one()  # assicurarsi che il metodo operi su un singolo record
        try:
            endpoint = self.name
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            auth = (self.user, self.password) if self.user and self.password else None
            content = content_data or self.content  # utilizzare content_data se disponibile, altrimenti utilizzare il contenuto del record
            method = self.method.lower()

            if method not in ['get', 'post', 'put', 'patch', 'delete']:
                _logger.error('Invalid HTTP method: %s', method)
                return {'error': 'Invalid HTTP method'}

            http_method = getattr(requests, method)
            result = http_method(endpoint, json=content, auth=auth, headers=headers)
            self.response = result.text  # salvare la risposta nel record
            return result.json()  # restituire la risposta come JSON
        except Exception as e:
            _logger.error('Error while making HTTP request: %s', str(e))
            self.response = str(e)  # salvare l'errore nel record
            return {'error': str(e)}


class MyController(http.Controller):
    _logger = logging.getLogger(__name__)  # Inizializzazione del logger

    @http.route('/custom_route', type='json', auth='user', methods=['POST'], csrf=False)
    def custom_route_handler(self, **post):
        try:
            # Converti la richiesta JSON in un dizionario Python
            data = json.loads(request.httprequest.data.decode('utf-8'))

            # Esegui operazioni solo se il type è "RESERVATION_CREATED"
            if data.get('type') == 'RESERVATION_CREATED':
                # Estrai i dettagli della prenotazione dal JSON
                booking_details = json.loads(data.get('content'))

                # Creazione di un record nel modello "account.move" con i dati ricevuti
                roombooking = request.env['account.move']
                new_booking = roombooking.create({
                    'refer': booking_details.get('refer'),
                    'checkin': booking_details.get('checkin'),
                    'checkout': booking_details.get('checkout'),
                    'totalGuest': booking_details.get('totalGuest'),
                    'totalChildren': booking_details.get('children'),
                    'totalInfants': booking_details.get('infants'),
                    'rooms': booking_details.get('rooms'),
                    'roomGross': booking_details.get('roomGross'),
                })

                self._logger.info('Nuova prenotazione creata con ID: %s', new_booking.id)

                # Qui, possiamo integrare la logica per inviare questi dati a un altro sistema o webhook, se necessario.
                api_config = request.env['solt.http.test'].sudo().search([], limit=1)
                if api_config:
                    api_config.action_request_with_structure(booking_details)

                return {'message': 'Dati della prenotazione creati con successo', 'id': new_booking.id}

            else:
                return {'message': 'Tipo di prenotazione non supportato'}

        except Exception as e:
            self._logger.error('Errore durante l\'elaborazione della prenotazione: %s', str(e))
            return {'error': str(e)}
#  ATTEMPT

# The key fingerprint is:
# SHA256:BC/D9FqkDfJwZ1gzkyceQ6r6Oymjmhe6EEzbrtnjGCE
# PS C:\Program Files\nodejs> & "C:\Users\giova\AppData\Roaming\npm\lt.cmd" --port 8069    
# your url is: https://honest-lemons-smell.loca.lt