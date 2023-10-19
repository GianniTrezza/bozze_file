from odoo import models, fields, api, _



class stanzeprenotate(models.Model):
    _name = 'stanze.prenotate'
    _description = 'Prenotazione stanze'

    refer = fields.Char(string='ID della Prenotazione')
    checkin = fields.Date(string='Data di Check-in')
    checkout = fields.Date(string='Data di Check-out')
    totalGuest = fields.Integer(string='Ospiti Totali')
    totalChildren = fields.Integer(string='Totali Ragazzi')
    totalInfants = fields.Integer(string='Totali Neonati')
    rooms = fields.Float(string='Numero stanza')
    roomGross = fields.Float(string='Costo stanza')
    state = fields.Selection(selection=[
        ('draft', 'In Bozza'),
        ('posted', 'Confermato'),
        ('cancel', 'Cancellato'),
    ], string='Stato', default='draft', readonly=False)

    tassa_soggiorno = fields.Float(string='Tassa di Soggiorno', compute='_calcolo_tassa_soggiorno', store=True)
    costo_pernotto = fields.Float(string='Costo Pernotto', compute='_calcolo_costo_pernotto', store=True)
    
    # seq_fatt = fields.Char("sequenza fattura")

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'stanze.prenotate.sequence')], limit=1)
        if sequence:
            next_accr = sequence.get_next_char(sequence.number_next_actual)
            sequence.sudo().write({'number_next': sequence.number_next + 1})
        else:
            next_accr = _('Nuova pratica')
        vals['refer'] = next_accr
        return super(stanzeprenotate, self).create(vals)
    

    def button_confirm_and_print(self):
        self.ensure_one()
        return self.env.ref('new_prenotazione.action_report_stanze_prenotate').report_action(self)


    
    @api.depends('checkin', 'checkout', 'totalGuest')
    def _calcolo_tassa_soggiorno(self):
        for record in self:
            if record.checkin and record.checkout and record.totalGuest:
                checkin_date = fields.Date.from_string(record.checkin)
                checkout_date = fields.Date.from_string(record.checkout)
                delta = checkout_date - checkin_date
                num_notti = delta.days
                record.tassa_soggiorno = 2 * num_notti * record.totalGuest


    @api.depends('rooms', 'roomGross')
    def _calcolo_costo_pernotto(self):
        for record in self:
            if record.rooms and record.roomGross:
                record.costo_pernotto = record.rooms * record.roomGross