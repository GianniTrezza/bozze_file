from odoo import models, fields, api, _

class DettaglioPrenotazione(models.Model):
    _name = 'dettaglio.prenotazione'
    _description = 'Dettaglio Prenotazione'

    tassa_soggiorno = fields.Float(string='Tassa di Soggiorno', compute='_calcolo_tassa_soggiorno', store=True)
    costo_pernotto = fields.Float(string='Costo Pernotto', compute='_calcolo_costo_pernotto', store=True)
    prenotazione_id = fields.Many2one('stanze.prenotate', string='Prenotazione')

    @api.depends('prenotazione_id.checkin', 'prenotazione_id.checkout', 'prenotazione_id.totalGuest')
    def _calcolo_tassa_soggiorno(self):
        for record in self:
            if record.prenotazione_id.checkin and record.prenotazione_id.checkout and record.prenotazione_id.totalGuest:
                checkin_date = fields.Date.from_string(record.prenotazione_id.checkin)
                checkout_date = fields.Date.from_string(record.prenotazione_id.checkout)
                delta = checkout_date - checkin_date
                num_notti = delta.days
                record.tassa_soggiorno = 2 * num_notti * record.prenotazione_id.totalGuest

    @api.depends('prenotazione_id.rooms', 'prenotazione_id.roomGross')
    def _calcolo_costo_pernotto(self):
        for record in self:
            if record.prenotazione_id.rooms and record.prenotazione_id.roomGross:
                record.costo_pernotto = record.prenotazione_id.rooms * record.prenotazione_id.roomGross


class StanzePrenotate(models.Model):
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

    dettaglio_line_ids = fields.One2many('dettaglio.prenotazione', 'prenotazione_id', string='Dettagli Prenotazione')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'stanze.prenotate.sequence')], limit=1)
        if sequence:
            next_accr = sequence.get_next_char(sequence.number_next_actual)
            sequence.sudo().write({'number_next': sequence.number_next + 1})
        else:
            next_accr = _('Nuova pratica')
        vals['refer'] = next_accr
        return super(StanzePrenotate, self).create(vals)

    def button_confirm_and_print(self):
        self.ensure_one()
        return self.env.ref('new_prenotazione.action_report_stanze_prenotate').report_action(self)
