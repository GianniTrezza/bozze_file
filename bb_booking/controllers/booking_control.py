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

class SoltHttpTest(models.Model):
    _name = 'solt.http.test'
    
    name = fields.Char('URL')
    method = fields.Selection([('post', 'POST'), ('get', 'GET'), ('put', 'PUT'), ('patch', 'PATCH'), ('delete', 'DELETE')], string='HTTP Method')
    user = fields.Char('User')
    password = fields.Char('Password')
    content = fields.Text('Content')
    response = fields.Text('Response')

    @api.multi
    def action_request(self, content_data=None):
        for test in self:
            endpoint = test.name
            headers = {
                'Content-Type': 'application/json', 
                'Accept': 'application/json',
            }
            
            auth = (test.user, test.password) if test.user and test.password else None
            content = test.content if not content_data else content_data
            result = getattr(requests, test.method)(endpoint, json=content, auth=auth, headers=headers)
            test.write({'response': result.text})


