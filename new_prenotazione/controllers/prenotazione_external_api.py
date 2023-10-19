from odoo import http
from odoo.http import request
import json

class collegamento_odoo(http.Controller):
    @http.route('/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def dati_ottenuti(self, **kwargs):
        data = request.jsonrequest

        if data:
            try:
                model = "stanze.prenotate"
                type = data.get('type')
                content_data = json.loads(data.get('content')) if data.get('content') else {}
                fields = {
                    'refer': content_data.get('refer'),
                    'checkin': content_data.get('checkin').split('T')[0] if content_data.get('checkin') else False,
                    'checkout': content_data.get('checkout').split('T')[0] if content_data.get('checkout') else False,
                    'totalGuest': content_data.get('totalGuest'),
                    'totalChildren': content_data.get('children'),
                    'totalInfants': content_data.get('infants'),
                    'rooms': content_data.get('rooms'),
                    'roomGross': content_data.get('roomGross'),
                }

                if type == 'RESERVATION_CREATED':
                    fields['state'] = 'draft'
                    record = request.env[model].create(fields)
                    return {'success': True, 'record_id': record.id}

                elif type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
                    refer_id = fields.get('refer')
                    record = request.env[model].search([('refer', '=', refer_id)])

                    if not record:
                        return {'error': 'No matching record found'}

                    new_state = 'cancel' if type == 'RESERVATION_CANCELLED' else 'posted'
                    record.write({'state': new_state})
                    return {'success': True, 'record_id': record.id}

                else:
                    return {'error': 'Invalid type'}

            except Exception as e:
                return {'error': str(e)}

        return {'error': 'Invalid data'}


