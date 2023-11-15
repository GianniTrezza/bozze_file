from odoo import http, models
from odoo import _
from odoo.http import request, Response
import json
import datetime
import logging

_logger = logging.getLogger(__name__)

class RoomBookingController(http.Controller):

    @http.route('/api/test', cors='*', auth='public', methods=['POST'], csrf=False)
    def handle_custom_endpoint(self, **post):
        json_data = request.httprequest.data
        data_dict = json.loads(json_data)
        content = json.loads(data_dict.get("content"))
        create_time_str = data_dict.get("createTime")

        try:
            create_time = datetime.datetime.strptime(create_time_str, '%Y-%m-%dT%H:%M:%SZ[UTC]') if create_time_str else None
        except ValueError:
            return Response("Invalid date format for createTime", content_type='text/plain', status=400)

        if not content.get("refer") or not content.get("guests"):
            return Response("Missing required fields", content_type='text/plain', status=400)

        checkin_str = content.get("guests")[0].get("checkin")
        checkout_str = content.get("guests")[0].get("checkout")
        
        try:
            checkin_date = datetime.datetime.strptime(checkin_str, '%Y-%m-%d').date() if checkin_str else None
            checkout_date = datetime.datetime.strptime(checkout_str, '%Y-%m-%d').date() if checkout_str else None
        except ValueError:
            return Response("Invalid date format", content_type='text/plain', status=400)

        reservation_data = {
            'partner_id': content.get("guestsList"),
            'email': content.get("guestMailAddress"),
            'refer': content.get("refer"),
            'ref': content.get('pmsProduct'),
            'roomName': content.get('roomName'),
            'checkin': checkin_date,
            'checkout': checkout_date,
            'channelNotes': content.get("channelNotes"),
            'totalGuest': content.get("totalGuest"),
            'totalChildren': content.get("totalChildren"),
            'totalInfants': content.get("totalInfants"),
            'rooms': content.get("rooms"),
            'roomGross': content.get("roomGross"),
            'invoicedate': create_time,
        }
        
        event_type = data_dict.get("type")
        response_data = {}

        if event_type == "RESERVATION_CREATED":
            invoice_details = self.calculate_invoice_details(reservation_data)
            self.create_invoice(reservation_data, invoice_details)
            response_data.update(invoice_details)
        elif event_type == "RESERVATION_CHANGE":
            refer_id = reservation_data.get('refer')
            nome_cliente=reservation_data.get('partner_id')

            invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id), ('partner_id', '=', nome_cliente)], limit=1)
            if not invoice_record:
                return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)
            # reservation_data.pop('partner_id', None)
            reservation_data.pop('email', None)
            if 'email' in request.env['account.move']._fields:
                invoice_record.sudo().write({'email': content.get("guestMailAddress")})

            # invoice_record.sudo().write(reservation_data)
            self.update_invoice_lines(invoice_record, reservation_data)
            response_data.update({
                "partner_id": invoice_record.partner_id.name,
                "move_id": invoice_record.id,
                "checkin": invoice_record.checkin.strftime('%Y-%m-%d') if isinstance(invoice_record.checkin, datetime.date) else invoice_record.checkin,
                "checkout": invoice_record.checkout.strftime('%Y-%m-%d') if isinstance(invoice_record.checkout, datetime.date) else invoice_record.checkout,
                "invoice_date": invoice_record.invoice_date.strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(invoice_record.invoice_date, datetime.datetime) else invoice_record.invoice_date,
                "totalGuest": invoice_record.totalGuest,
                "totalChildren": invoice_record.totalChildren,
                "totalInfants": invoice_record.totalInfants,
                "rooms": invoice_record.rooms,
                "product_id": invoice_record.roomName,
                "note aggiuntive": invoice_record.channelNotes,
                "ref":invoice_record.pmsProduct,
                "state": invoice_record.state, 
            })
        elif event_type in ['RESERVATION_CANCELLED', 'RESERVATION_CONFIRMED']:
            refer_id = reservation_data.get('refer')
            checkout_id=reservation_data.get('checkout')
            
            invoice_record = request.env['account.move'].sudo().search([('refer', '=', refer_id)], limit=1)
            if not invoice_record:
                return Response(f"No invoice found with refer: {refer_id}", content_type='text/plain', status=404)

            if invoice_record.checkout != checkout_id:
                return Response(f"Invoice found with refer: {refer_id}, but with different checkout date.", content_type='text/plain', status=400)

            new_state = 'cancel' if event_type == 'RESERVATION_CANCELLED' else 'posted'
            invoice_record.sudo().write({'state': new_state})
        else:
            return Response("Invalid event type", content_type='text/plain', status=400)
        
        for key, value in response_data.items():
            if isinstance(value, datetime.date):
                response_data[key] = value.strftime('%Y-%m-%d')

        return Response(json.dumps(response_data), content_type='application/json', status=200)

    def calculate_invoice_details(self, reservation_data):
        nome_ospite= reservation_data['partner_id']
        checkin_date = reservation_data['checkin']
        
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        num_ospiti = reservation_data['totalGuest']

        tourist_tax_quantity = num_notti * num_ospiti * 2
        
        booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
        booking_quantity = reservation_data['rooms']
        booking_price_unit = reservation_data['roomGross']
        nome_stanza = reservation_data['roomName']
    
        return {
            "Orario creazione prenotazione": reservation_data["invoicedate"].strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(reservation_data["invoicedate"], datetime.datetime) else reservation_data["invoicedate"],
            "Nome ospite": nome_ospite,
            "Valore tassa turistica": tourist_tax_quantity,
            "Identificativo della prenotazione": booking_name,
            "Numero stanze": booking_quantity,
            "Costo stanza": booking_price_unit,
            "Tipologia stanza": nome_stanza,
            "Numero identificativo Camera": reservation_data["ref"]
            
        }
    def create_invoice(self, reservation_data, invoice_details):
        tax_0_percent = None
        partner_name = reservation_data['partner_id']
        nome_stanza = reservation_data['roomName']
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        # partner = request.env['res.partner'].sudo().search([('name', '=', partner_name)], limit=1)
        partner = request.env['res.partner'].sudo().with_context(partner_display='invoice_partner_display_name').search([('name', '=', partner_name)], limit=1)

        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': partner_name,
                'email': reservation_data.get('email'),
                'customer_rank': 1
            })

        room_product = request.env['product.product'].sudo().search([('name', '=', nome_stanza)])
        if not room_product:
            room_product = request.env['product.product'].sudo().create({'name': nome_stanza})
            
        tassa_soggiorno_product = request.env['product.product'].sudo().search([('name', '=', 'Tassa di Soggiorno')], limit=1)
        if not tassa_soggiorno_product:
            tax_0_percent = request.env['account.tax'].sudo().search(
                [('amount_type', '=', 'percent'), ('type_tax_use', '=', 'sale'), ('amount', '=', 0)],
                limit=1
            )
            if not tax_0_percent:
                raise ValueError("Non esiste un'imposta al 0% nel sistema. Creala o assegnala manualmente.")
            
            vals = {
                'name': 'Tassa di Soggiorno',
                'type': 'service',
            }
            
            if tax_0_percent is not None:
                vals['taxes_id'] = [(6, 0, [tax_0_percent.id])]

            tassa_soggiorno_product = request.env['product.product'].sudo().create(vals)
        # FINE RETTIFICA
        customer_invoice_journal = request.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
        account_id = customer_invoice_journal.default_account_id.id if hasattr(customer_invoice_journal, 'default_account_id') else 44
        journal_id = customer_invoice_journal.id
        try:
            partner_values = {
                'name': reservation_data["partner_id"],
                'email': reservation_data["email"],
            }

            print(f"Il cliente presenta le seguenti features:", partner_values)
            partner = request.env['res.partner'].sudo().create(partner_values)
            print(f"Il cliente presenta il seguente ID:", partner)
            _logger.debug("Partner ID: %s", partner.id)

            partner_display_name = partner.name_get()[0][1] if partner else "Nuovo Partner"
            
            invoice_values = {
                'journal_id': journal_id,
                'move_type': 'out_invoice',
                'ref': reservation_data['ref'],
                'partner_id': partner.id,
                'invoice_partner_display_name': partner_display_name,
                'checkin': reservation_data['checkin'],
                'checkout': reservation_data['checkout'],
                'refer': reservation_data['refer'],
                'totalGuest': reservation_data['totalGuest'],
                'totalChildren': reservation_data['totalChildren'],
                'rooms': reservation_data['rooms'],
                'roomGross': reservation_data['roomGross'],
                'invoice_date': reservation_data['invoicedate'],
                'channelNotes': reservation_data['channelNotes'],
            }
            invoice_record = request.env['account.move'].sudo().create(invoice_values)
            # invoice_record.message_post(
            #     body=f"<p><b><font size='4' face='Arial'>Dati di fatturazione creati:</font></b><br>"
            #         f"Nome Cliente: {reservation_data['partner_id']}<br>"
            #         f"Refer: {reservation_data['refer']}<br>"
            #         f"Data Fattura: {reservation_data['invoicedate']}<br>"
            #         f"Checkin: {checkin_date}<br>"
            #         f"Checkout: {checkout_date}<br>"
            #         f"Nome stanza: {nome_stanza}<br></p>"
            #         f"Note stanza aggiuntive: {reservation_data['channelNotes']}<br>"
            #         f"Numero bambini: {reservation_data['totalChildren']}<br>"
            #         f"Ospiti: {reservation_data['totalGuest']}<br>"
            #         f"Prezzo totale: {reservation_data['roomGross']}<br>",
            #     message_type='comment'
            # )
        except Exception as e:
            _logger.error("Impossibile creare la fattura: %s", str(e))
            return Response("Errore interno del server", content_type='text/plain', status=500)

        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        delta = checkout_date - checkin_date
        num_notti = delta.days


        booking_line_values = {
            'move_id': invoice_record.id,
            'product_id': room_product.id,
            'name': invoice_details['Identificativo della prenotazione'],
            'quantity': reservation_data['rooms'],
            'price_unit': invoice_details['Costo stanza'],
            'account_id': account_id
        }
        request.env['account.move.line'].sudo().create(booking_line_values)

        tourist_tax_line_values = {
            'move_id': invoice_record.id,
            'product_id': tassa_soggiorno_product.id,
            'name': "Tassa soggiorno",
            'quantity': reservation_data['totalGuest']*num_notti,
            'price_unit': 2,
            'account_id': account_id
        }
        
        request.env['account.move.line'].sudo().create(tourist_tax_line_values)
    def update_invoice_lines(self, invoice_record, reservation_data):
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        checkin_date = reservation_data['checkin']
        checkout_date = reservation_data['checkout']
        total_guest = reservation_data['totalGuest']
        total_children = reservation_data['totalChildren']
        rooms = reservation_data['rooms']
        room_gross= reservation_data['roomGross']
        room_name_guest= reservation_data['ref']
        delta = checkout_date - checkin_date
        num_notti = delta.days
        formatted_invoice_date = reservation_data['invoicedate'].strftime('%Y-%m-%d') if isinstance(reservation_data['invoicedate'], datetime.datetime) else reservation_data['invoicedate']
        
        update_values = {
            'invoice_date': formatted_invoice_date,
            'checkin': checkin_date,
            'checkout': checkout_date, 
            'totalGuest': total_guest,
            'totalChildren':total_children,
            'rooms': rooms,
            'roomGross': room_gross, 
            'ref': room_name_guest,
            'channelNotes': reservation_data['channelNotes']
        }
            # Dictionary to track changes for chatter
        changes = {}

        # Check for changes and add them to the changes dictionary
        fields_to_check = ['invoice_date', 'checkin', 'checkout', 'totalGuest', 'totalChildren', 'rooms', 'roomGross', 'ref', 'channelNotes']
        # for field in fields_to_check:
        #     new_value = reservation_data.get(field)
        #     old_value = getattr(invoice_record, field, None)
        #     if new_value != old_value:
        #         formatted_new_value = new_value.strftime('%Y-%m-%d') if isinstance(new_value, datetime.date) else new_value
        #         changes[field] = formatted_new_value
        for field in fields_to_check:
            new_value = reservation_data.get(field)
            if new_value is None:
                continue
            old_value = getattr(invoice_record, field, None)
            if new_value != old_value:
                formatted_new_value = new_value.strftime('%Y-%m-%d') if isinstance(new_value, datetime.date) else new_value
                changes[field] = formatted_new_value

        # Update the invoice record
        invoice_record.sudo().write({k: v for k, v in reservation_data.items() if k in fields_to_check})

        # Post only changes to the chatter
        if changes:
            change_messages = [f"{field}: {value}" for field, value in changes.items()]
            message_body = "<p><b><font size='4' face='Arial'>Updated Data:</font></b><br>" + "<br>".join(change_messages) + "</p>"
            invoice_record.message_post(body=message_body, message_type='comment')
# *********************************************GESTIONE DATI AGGIORNATI: vecchio codice************************************
        # changes = {}

        # for field, value in update_values.items():
        #     if getattr(invoice_record, field) != value:
        #         changes[field] = value

        # invoice_record.sudo().write(update_values)

        
        # if changes:
        #     change_messages = []
        #     for field, value in changes.items():
        #         display_value = value.strftime('%Y-%m-%d') if isinstance(value, datetime.date) else value
        #         change_messages.append(f"{field}: {display_value}")
        #     message_body = "<p><b><font size='4' face='Arial'>I dati aggiornati sono i seguenti:</font></b><br>" + "<br>".join(change_messages) + "</p>"
        #     invoice_record.message_post(body=message_body, message_type='comment')
        
        # invoice_record.sudo().write(update_values)
        # invoice_record.message_post(
        #         body=f"<p><b><font size='4' face='Arial'>Dati aggiornati:</font></b><br>"
        #             f"Nome Cliente: {reservation_data['partner_id']}<br>"
        #             f"Refer: {reservation_data['refer']}<br>"
        #             f"Data Fattura: {reservation_data['invoicedate']}<br>"
        #             f"Checkin: {checkin_date}<br>"
        #             f"Checkout: {checkout_date}<br>"
        #             f"Nome stanza: {reservation_data['roomName']}<br></p>"
        #             f"Note stanza aggiuntive: {reservation_data['channelNotes']}<br>"
        #             f"Numero bambini: {reservation_data['totalChildren']}<br>"
        #             f"Ospiti: {reservation_data['totalGuest']}<br>"
        #             f"Prezzo unitario: {reservation_data['roomGross']}<br>",
        #         message_type='comment'
        #     )
        
        booking_name = f"Prenotazione {reservation_data['refer']} dal {reservation_data['checkin']} al {reservation_data['checkout']}"
        for line in invoice_record.invoice_line_ids:
            if line.product_id.name == reservation_data['roomName']:
                line.write({'name': booking_name})
                line.write({'price_unit': reservation_data['roomGross']})
                line.write({'quantity': reservation_data['rooms']})
            elif line.product_id.name == 'Tassa di Soggiorno':
                line.write({'quantity': reservation_data['totalGuest'] * num_notti})
                line.write({'price_unit': 2})
                pass
