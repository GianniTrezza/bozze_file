from odoo import api, fields, models, _
from datetime import datetime

#Fields legati alle info prenotazioni presenti nel file excel
class Booking(models.Model):
    _name = 'prenotazione.stanze'
    _description = 'Informazioni sulle stanze prenotate'
    _order = "createTime desc"
    # _order = "soggiorno_input desc"


    refer = fields.Char(string='Codice') #ID Prenotazione
    status = fields.Selection([
        ('pending', 'In approvazione'),
        ('confirmed', 'Confermato'),
        ('cancelled', 'Cancellato'),
    ], string='Stato')
    # Nel tasto Stato deve comparire sia lo stato generale, sia lo stato del pagamento
    structure_name= fields.Char(string ="Nome Struttura")
    # bookingtime= fields.Datetime(string="Data Prenotazione")
    checkin = fields.Datetime(string='Orario Check In') #Data e orario check In
    checkout = fields.Datetime(string='Orario Check Out') #Data e orario check in
    createTime = fields.Datetime(string='Data di creazione') #Data di creazione
    updateTime = fields.Datetime(string='Data di aggiornamento') #Data di aggiornamento
    channelNotes = fields.Text(string='Nota opzionale') #Nota opzionale che si può aggiungere alla prenotazione
    children = fields.Integer(string='Numero di ragazzi') #Numero di ragazzi
    infants = fields.Integer(string='Numero di neonati') #Numero di infanti
    phone = fields.Char(string='Numero di telefono') #Numero di telefono
    roomGross = fields.Float(string='Costo stanza') #Costo stanza
    totalGross = fields.Float(string='Costo Totale') #Costo Totale
    totalGuest = fields.Integer(string='Ospiti totali') #Ospiti totali

    arrivalTime = fields.Datetime(string='Orario di Arrivo')
    channelName = fields.Char(string='Nome del Canale di prenotazione') #i.e. AirBnB
    currency = fields.Char(string='Valuta Moneta')
    Name = fields.Char(string='Cliente') #Aggiungere res.partners
    guestMailAddress = fields.Char(string='Email Address')
    id = fields.Integer(string='Booking Numeric ID')
    paymentStatus = fields.Selection([
        ('unpaid', 'Pagato'),
        ('paid', 'Non Pagato'),
    ], string='Payment Status')
    paymentType = fields.Char(string='Tipo di pagamento')
    product = fields.Char(string='Room ID')
    roomName = fields.Char(string='Camera')
    rooms = fields.Integer(string='Numero Stanze')
    totalChildren = fields.Integer(string='Numero dei ragazzi totali')
    totalnfants = fields.Integer(string='Numero di neonati totali')
    totalPaid = fields.Float(string='Totale pagato')
    touristTax = fields.Float(string='Tassa turistica')

    soggiorno_input = fields.Html(string='Soggiorno', compute='_compute_soggiorno_input', sanitize=False, store=False)

    # soggiorno_input = fields.Char(string='Soggiorno', compute='_compute_soggiorno_input',  store=True)
    # inverse='_set_soggiorno_input',
    data_ingresso = fields.Date(string='Data di Ingresso', compute='_compute_date')
    data_uscita = fields.Date(string="Data d'Uscita", compute='_compute_date')
    display_status = fields.Html(string='Stato visualizzato', compute='_compute_display_status', sanitize=False, store=False)

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'prenotazione.stanze.sequence')], limit=1)
        
        if sequence:
            next_prenotazione = sequence.get_next_char(sequence.number_next_actual)
            sequence.sudo().write({'number_next': sequence.number_next + 1})
        else:
            next_prenotazione = _('Nuova prenotazione')
        
        vals['refer'] = next_prenotazione
        
        return super(Booking, self).create(vals)
    
    # @api.model
    # def create(self, vals):
    #     sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'hospital.accreditation.sequence')], limit=1)
    #     if sequence:
    #         next_accr = sequence.get_next_char(sequence.number_next_actual)
    #         sequence.sudo().write({'number_next': sequence.number_next + 1})
    #     else:
    #         next_accr = _('Nuova pratica')
    #     vals['name'] = next_accr
    #     vals['codice_pratica'] = next_accr
    #     return super(HospitalAccreditation, self).create(vals)

    
    @api.depends('data_ingresso', 'data_uscita')
    def _compute_soggiorno_input(self):
        for record in self:
            if record.data_ingresso and record.data_uscita:
                intervallo = (record.data_uscita - record.data_ingresso).days + 1
                record.soggiorno_input = f"Ingresso: {record.data_ingresso} <br/> Uscita: {record.data_uscita} <br/> Permanenza: {intervallo} giorni"
            else:
                record.soggiorno_input = "" 



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

    # @api.depends('status', 'paymentStatus')
    # def _compute_display_status(self):
    #     for record in self:
    #         stato_generico = dict(self._fields['status'].selection).get(record.status, "")
    #         stato_pagamento = dict(self._fields['paymentStatus'].selection).get(record.paymentStatus, "")

    #         combined = []
    #         if stato_generico:
    #             combined.append(stato_generico)
    #         if stato_pagamento:
    #             combined.append(stato_pagamento)

    #         record.display_status = " - ".join(combined)






    
