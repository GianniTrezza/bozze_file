# class OdooController(http.Controller):
#     @http.route('/odoo_controller/odoo_controller/',auth='public')
#     def index(self, **kw):
#         return "Hello, world"

from odoo import http
from odoo.http import request, Response
import json
import datetime

class RoomBookingController(http.Controller):
    @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
    def handle_custom_endpoint(self, **post):
        json_data = request.httprequest.data
        data_dict = json.loads(json_data)
        content = json.loads(data_dict.get("content"))
        type = data_dict.get("type")

        # Validazione dei dati in entrata
        if not content.get("refer") or not content.get("guests"):
            return Response("Missing required fields", content_type='text/plain', status=400)

        checkin_str = content.get("guests")[0].get("checkin")
        checkout_str = content.get("guests")[0].get("checkout")

        # Convalida e conversione delle date
        try:
            checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
            checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
        except ValueError:
            return Response("Invalid date format", content_type='text/plain', status=400)

        reservation_data = {
            'refer': content.get("refer"),
            'checkin': checkin_date,
            'checkout': checkout_date,
            'totalGuest': content.get("totalGuest"),
            'totalChildren': content.get("totalChildren"),
            'totalInfants': content.get("totalInfants"),
            'rooms': content.get("rooms"),
            'roomGross': content.get("roomGross")

        }


        model = 'stanze.prenotate' 

        if type == 'RESERVATION_CREATED':
            partner = request.env['res.partner'].sudo().search([('name', '=', content.get("partner_name"))], limit=1)
            if partner:
                reservation_data['partner_id'] = partner.id
            new_move = request.env[model].sudo().create(reservation_data)
            response_data = {
                "move_id": new_move.id,
                "refer": new_move.refer,
                "checkin": new_move.checkin.strftime('%Y-%m-%d') if isinstance(new_move.checkin, datetime.date) else new_move.checkin,
                "checkout": new_move.checkout.strftime('%Y-%m-%d') if isinstance(new_move.checkout, datetime.date) else new_move.checkout,
                "totalGuest": new_move.totalGuest,
                "totalChildren": new_move.totalChildren,
                "totalInfants": new_move.totalInfants,
                "rooms": new_move.rooms,
                "roomGross": new_move.roomGross,
                "state": new_move.state,
            }

        elif type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
            refer_id = reservation_data.get('refer')
            record = request.env[model].sudo().search([('refer', '=', refer_id)], limit=1)
            new_state = 'cancel' if type == 'RESERVATION_CANCELLED' else 'posted'
            record.sudo().write({'state': new_state})
            response_data = {
                "move_id": record.id,
                "refer": record.refer,
                "checkin": record.checkin.strftime('%Y-%m-%d') if isinstance(record.checkin, datetime.date) else record.checkin,
                "checkout": record.checkout.strftime('%Y-%m-%d') if isinstance(record.checkout, datetime.date) else record.checkout,
                "totalGuest": record.totalGuest,
                "totalChildren": record.totalChildren,
                "totalInfants": record.totalInfants,
                "rooms": record.rooms,
                "roomGross": record.roomGross,
                "state": record.state, 
            }

        else:
            return Response("Invalid type", content_type='text/plain', status=400)

        return Response(json.dumps(response_data), content_type='application/json')


