from odoo import http
from odoo.http import request

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
        invoice = room_booking.create_invoice_from_webhook(data)

        return {"message": "Data received and saved successfully"}
