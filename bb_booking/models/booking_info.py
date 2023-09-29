from odoo import models, fields

class roombooking(models.Model):
    _inherit = "account.move"

    # INFORMAZIONI GENERALI DELLA PRENOTAZIONE
    refer = fields.Char(string='ID Prenotazione')
    status = fields.Selection([
        ('pending', 'In approvazione'),
        ('confirmed', 'Confermato'),
        ('cancelled', 'Cancellato'),
    ], string='Stato')
    checkin = fields.Datetime(string='Data e Ora di Check-in')
    checkout = fields.Datetime(string='Data e Ora di Check-out')
    createTime = fields.Datetime(string='Data di Creazione')
    updateTime = fields.Datetime(string='Data di Aggiornamento')
    channelNotes = fields.Text(string='Note del Canale')
    children = fields.Integer(string='Numero di Ragazzi')
    infants = fields.Integer(string='Numero di Neonati')
    phone = fields.Char(string='Numero di Telefono')
    roomGross = fields.Float(string='Costo Stanza')
    totalGross = fields.Float(string='Costo Totale')
    totalGuest = fields.Integer(string='Ospiti Totali')
    
    # ALTRE INFORMAZIONI DELLA PRENOTAZIONE
    arrivalTime = fields.Char(string='Orario di Arrivo')
    channelName = fields.Char(string='Nome Canale di Prenotazione')
    currency = fields.Char(string='Valuta')
    firstName = fields.Char(string='Nome')
    guestMailAddress = fields.Char(string='Indirizzo Email')
    booking_id = fields.Integer(string='ID Prenotazione')
    lastName = fields.Char(string='Cognome')
    paymentStatus = fields.Char(string='Stato del Pagamento')
    paymentType = fields.Char(string='Metodo di Pagamento')
    product_id = fields.Many2one('product.product', string='Prodotto')
    roomName = fields.Char(string='Nome Stanza')
    rooms = fields.Integer(string='Numero di Stanze')
    totalChildren = fields.Integer(string='Totali Ragazzi')
    totalInfants = fields.Integer(string='Totali Neonati')
    totalPaid = fields.Float(string='Totale Pagato')
    touristTax = fields.Float(string='Tassa Turistica')