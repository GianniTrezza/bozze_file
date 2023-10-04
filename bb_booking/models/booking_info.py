from odoo import models, fields,_ , api

class roombooking(models.Model):

    _inherit = "account.move"

    # INFORMAZIONI GENERALI DELLA PRENOTAZIONE
    # refer = fields.Char(string='ID Prenotazione')
    status = fields.Selection([
        ('pending', 'In approvazione'),
        ('confirmed', 'Confermato'),
        ('cancelled', 'Cancellato'),
    ], string='Stato')
    checkin = fields.Datetime(string='Data e Ora di Check-in')
    checkout = fields.Datetime(string='Data e Ora di Check-out')
    createTime = fields.Datetime(string='Data di Creazione')
    updateTime = fields.Datetime(string='Data di Aggiornamento')
    
    children = fields.Integer(string='Numero di Ragazzi')
    infants = fields.Integer(string='Numero di Neonati')
    phone = fields.Char(string='Numero di Telefono')
    
    totalGross = fields.Float(string='Costo Totale')
    totalGuest = fields.Integer(string='Ospiti Totali')
    
    # ALTRE INFORMAZIONI DELLA PRENOTAZIONE
    data_ingresso = fields.Date(string='Data di Ingresso', compute='_compute_date')
    data_uscita = fields.Date(string="Data d'Uscita", compute='_compute_date')
    # arrivalTime = fields.Char(string='Orario di Arrivo')
    channelName = fields.Char(string='Nome Canale di Prenotazione')
    currency = fields.Selection([
        ('eur', 'EUR'),
        ('usdol', 'USDOL'),
    ], string='Currency')
    firstName = fields.Char(string='Nome')
    guestMailAddress = fields.Char(string='Indirizzo Email')
    booking_id = fields.Integer(string='ID Prenotazione')
    lastName = fields.Char(string='Cognome')
    paymentStatus = fields.Selection([
        ('unpaid', 'Pagato'),
        ('paid', 'Non Pagato'),
    ], string='Stato del Pagamento')
    
    paymentType = fields.Char(string='Metodo di Pagamento')
    # product_id = fields.Many2one('product.product', string='Prodotto')
    # rooms = fields.Integer(string='Numero di Stanze')
    # roomName = fields.Char(string='Nome Stanza')
    totalChildren = fields.Integer(string='Totali Ragazzi')
    totalInfants = fields.Integer(string='Totali Neonati')
    display_status = fields.Html(string='Stato visualizzato', compute='_compute_display_status', sanitize=False, store=False)
    soggiorno_input = fields.Html(string='Soggiorno', compute='_compute_soggiorno_input', sanitize=False, store=False)

    @api.depends('checkin', 'checkout')
    def _compute_date(self):
        for record in self:
            record.data_ingresso = record.checkin.date() if record.checkin else False
            record.data_uscita = record.checkout.date() if record.checkout else False

    

    @api.depends('status', 'paymentStatus')
    def _compute_display_status(self):
        for record in self:
            stato_generico = dict(self._fields['status'].selection).get(record.status, "")
            stato_pagamento = dict(self._fields['paymentStatus'].selection).get(record.paymentStatus, "")

            combined = [
                f"Stato: {stato_generico}" if stato_generico else "",
                f"Stato Pagamento: {stato_pagamento}" if stato_pagamento else ""
            ]

            record.display_status = "<br/>".join(filter(None, combined))

    @api.depends('data_ingresso', 'data_uscita')
    def _compute_soggiorno_input(self):
        for record in self:
            if record.data_ingresso and record.data_uscita:
                intervallo = (record.data_uscita - record.data_ingresso).days + 1
                record.soggiorno_input = f"Ingresso: {record.data_ingresso} <br/> Uscita: {record.data_uscita} <br/> Permanenza: {intervallo} giorni"
            else:
                record.soggiorno_input = ""

class prenotadettagli(models.Model):

    _inherit = "account.move.line"

    roomName = fields.Many2one ('product.product', string='Nome Stanza')
    channelNotes = fields.Text(string='Note del Canale')
    data_ingresso = fields.Date(string='Data di Ingresso', compute='_compute_date')
    data_uscita = fields.Date(string="Data d'Uscita", compute='_compute_date')
    rooms = fields.Integer(string='Numero di Stanze')
    
    roomGross = fields.Float(string='Costo Stanza')
    touristTax = fields.Float(string='Tassa Turistica')
    # tassa di soggiorno= (creare una funzione che prenda come campi numero infanti, neonati, che calcoli il numero totale di ospiti e che moltiplichi il totale per 2 euro
    totalPaid = fields.Float(string='Totale Pagato')

    



