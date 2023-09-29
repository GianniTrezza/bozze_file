from odoo import api, fields, models

class RoomBooking(models.Model):
    _name = 'room.booking'
    _description = 'Room Booking Information'

    refer = fields.Char('ID Prenotazione')
    status = fields.Char('Stato Prenotazione')
    checkin = fields.Datetime('Check In')
    checkout = fields.Datetime('Check Out')
    createTime = fields.Datetime('Data Creazione')
    updateTime = fields.Datetime('Data Aggiornamento')
    channelNotes = fields.Text('Nota Prenotazione')
    children = fields.Integer('Numero di Ragazzi')
    infants = fields.Integer('Numero di Neonati')
    phone = fields.Char('Telefono')
    roomGross = fields.Float('Costo Stanza')
    totalGross = fields.Float('Costo Totale')
    totalGuest = fields.Integer('Ospiti Totali')
    arrivalTime = fields.Char('Orario di Arrivo')
    channelName = fields.Char('Nome Canale Prenotazione')
    currency = fields.Char('Valuta')
    firstName = fields.Char('Nome Cliente')
    guestMailAddress = fields.Char('Indirizzo Email Cliente')
    id = fields.Integer('ID Prenotazione Numerico')
    lastName = fields.Char('Cognome Cliente')
    paymentStatus = fields.Char('Stato del Pagamento')
    paymentType = fields.Char('Metodo di Pagamento')
    product = fields.Many2one('product.product', string='Prodotto Stanza')
    roomName = fields.Char('Nome Stanza')
    rooms = fields.Integer('Numero Stanze')
    totalChildren = fields.Integer('Numero Totale Ragazzi')
    totalInfants = fields.Integer('Numero Totale Neonati')
    totalPaid = fields.Float('Totale Pagato')
    touristTax = fields.Float('Tassa Turistica')
    

    @api.model
    def create_invoice_from_webhook(self, data):
        product_pernotto = self.env['product.product'].search([('default_code', '=', 'PERNOTTO')], limit=1)
        product_tasse = self.env['product.product'].search([('default_code', '=', 'TASSE')], limit=1)
        
        if not product_pernotto or not product_tasse:
            return
        
        invoice_vals = {
            'partner_id': 1, # ID del partner (cliente) - da determinare in base ai tuoi requisiti
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': product_pernotto.id,
                    'name': data.get('roomName'),
                    'quantity': data.get('rooms', 1),
                    'price_unit': data.get('roomGross', 0.0),
                }),
                (0, 0, {
                    'product_id': product_tasse.id,
                    'name': 'Tassa di Soggiorno',
                    'quantity': 1,
                    'price_unit': data.get('touristTax', 0.0),
                }),
            ]
        }
        
        invoice = self.env['account.move'].create(invoice_vals)
        return invoice

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_room = fields.Many2one('product.product', string="Room Product")
    tourist_tax = fields.Float(string="Tourist Tax")
