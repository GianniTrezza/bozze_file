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




# \"accommodation\":{\"address\":\"via filippo caruso\",\"checkinEnd\":20,\"checkinStart\":12,\"checkout\":12,\"city\":\"ROMA\",\"currency\":\"EUR\",\"id\":\"557782\",\"latitude\":41.8489657,\"longitude\":12.5764685,\"name\":\"OdooERP  Test Api Building L.A.\",\"phoneNumber\":\"+3906060606\",\"timeZone\":\"Europe/Rome\",\"timeZoneOffset\":\"+01:00\",\"zipCode\":\"00173\"}


