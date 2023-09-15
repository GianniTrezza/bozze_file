from odoo import models, api, fields, _

class ResPartner(models.Model):
    _inherit = "res.partner"
    e_accreditata = fields.Boolean(string='Accreditata')
    is_struttura_sanitaria = fields.Boolean(string='Struttura Sanitaria', default=False)


class HospitalAccreditation(models.Model):
    _name = 'hospital.accreditation'
    _description = 'Accreditamento delle Strutture Sanitarie'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _order = "create_date desc"

    def _get_default_user(self):
        return self.env.user.id
    
    name = fields.Char(string='Name', required=True, copy=False)
    codice_pratica = fields.Char(string='Codice Pratica', readonly=True, copy=False, default=lambda self: _('Nuova pratica'))
    autore_reg_id = fields.Many2one('res.users', string='Autore Registrazione', default=_get_default_user, readonly=True)
    tipologia_pratica_id = fields.Many2one('hospital.tipologia_pratica', string='Tipologia Pratica', required=True)
    richiedente_id = fields.Many2one('res.partner', string='Richiedente', domain=[('is_company', '=', False), ('is_struttura_sanitaria', '=', False)], required=True)
    struttura_da_accreditare_id = fields.Many2one('res.partner', string='Struttura da Accreditare', domain=[('is_company', '=', True), ('is_struttura_sanitaria', '=', True), ('e_accreditata', '=', False)], required=True)

    descrizione = fields.Html(string='Descrizione')
    state = fields.Selection([
        ('draft', 'In Compilazione'),
        # ('in_progress', 'In Progress'),
        ('to_be_approved', 'Da Approvare'),
        ('approved', 'Approvato'),
        ('refused', 'Rifiutato'),
    ], default='draft', readonly= True, track_visibility='onchange')
    Incremento = fields.Integer('Incremento', default=1)
    year_from_code = fields.Char(string='Anno dal codice pratica', compute='_compute_year_from_code', store=True)

    @api.depends('codice_pratica')
    def _compute_year_from_code(self):
        for rec in self:
            if rec.codice_pratica and '/' in rec.codice_pratica:
                rec.year_from_code = rec.codice_pratica.split('/')[1]
            else:
                rec.year_from_code = False


    @api.model
    def create(self, vals):
        if not vals.get('Incremento'):
            max_incremento = self.search([], order="Incremento desc", limit=1)
            new_incremento = max_incremento.Incremento + 1 if max_incremento else 1
            vals['Incremento'] = new_incremento

        nome_formattato = f'ACCR/{fields.Date.today().year}/{str(vals["Incremento"]).zfill(5)}'
        vals['name'] = nome_formattato
        vals['codice_pratica'] = nome_formattato

        return super(HospitalAccreditation, self).create(vals)
    def action_recorded(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.accreditation',
            'view_mode': 'form',
            'view_id': self.env.ref('new_accreditamento.view_accreditation_form').id,

            'res_id': self.id,
        }

    def action_to_be_approved(self):
        self.write({'state': 'to_be_approved'})
        return True
    
    def action_approve(self):
        self.write({'state': 'approved'})
        for record in self:
            if record.struttura_da_accreditare_id:
                record.struttura_da_accreditare_id.write({
                    'e_accreditata': True 
                })
        # return self.env.ref('new_accreditamento.action_accreditation').read()[0]
    def action_refuse(self):
        self.write({'state': 'refused'})
        for record in self:
            if record.struttura_da_accreditare_id:
                record.struttura_da_accreditare_id.write({
                    'e_accreditata': False
                })
        # return self.env.ref('new_accreditamento.action_accreditation').read()[0]

    def action_forward(self):
        self.write({'state': 'to_be_approved'})
        return True
    def action_backward(self):
        self.state== "draft"
        return True
    
    # Vecchio codice
    # def action_backward(self):
    #     self.write({'state': ['draft', 'in_progress', 'to_be_approved', 'approved', 'refused']})
    #     return True
    
#FIX DA FARE
# 1) Gestione dei duplicate: in particolare, ottenere, premendo Duplicate, la pratica nello stato "In compilazione", con i seguenti records già compilati:
# richiedente, codice pratica e autore registrazione: quelli da compilarsi devono essere solo descrizione e Struttura sanitaria
# 2) Elimininazione del flag "è una struttura sanitaria" dalla lista delle "Strutture Sanitarie"
# 3) ripristinare ir_sequence_data.xml
# 4) Far sì che il numero della pratica compaia all'interno del sheet
# 5) Togliere tasto "Da approvare" ed "In progress"
    





