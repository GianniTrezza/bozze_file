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
    struttura_da_accreditare_id = fields.Many2one('res.partner', string='Struttura da Accreditare', domain=[('is_company', '=', True), ('is_struttura_sanitaria', '=', True), ('e_accreditata', '=', False)])

    descrizione = fields.Html(string='Descrizione')
    state = fields.Selection([
        ('draft', 'In Compilazione'),
        ('to_be_approved', 'Da Approvare'),
        ('approved', 'Approvato'),
        ('refused', 'Rifiutato'),
    ], default='draft', readonly= True, track_visibility='onchange')

    year_from_code = fields.Char(string='Anno dal codice pratica', compute='_compute_year_from_code', store=True)
    acc_number = fields.Char(string='Accreditation Number', readonly=True)

    @api.depends('codice_pratica')
    def _compute_year_from_code(self):
        for rec in self:
            if rec.codice_pratica and '/' in rec.codice_pratica:
                rec.year_from_code = rec.codice_pratica.split('/')[1]
            else:
                rec.year_from_code = False
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'hospital.accreditation.sequence')], limit=1)
        if sequence:
            next_accr = sequence.get_next_char(sequence.number_next_actual)
            sequence.sudo().write({'number_next': sequence.number_next + 1})
        else:
            next_accr = _('Nuova pratica')

        vals['name'] = next_accr
        vals['codice_pratica'] = next_accr

        return super(HospitalAccreditation, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'hospital.accreditation.sequence')], limit=1)
        if sequence:
            next_accr = sequence.get_next_char(sequence.number_next_actual)
            # sequence.sudo().write({'number_next': sequence.number_next + 1})
        else:
            next_accr = _('Nuova pratica')

        default.update({
            'name': next_accr,
            'codice_pratica': next_accr,
            'state': 'draft',
            'descrizione': False,
            'struttura_da_accreditare_id': False,
        })

        return super(HospitalAccreditation, self).copy(default)
    def unlink(self):
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'hospital.accreditation.sequence')], limit=1)
        if sequence:
            # Controlla quanti record ci sono nella tabella delle pratiche
            record_count = self.search_count([])

            # Se stai cercando di eliminare tutti i record, reimposta il contatore a 1
            if record_count <= len(self):
                sequence.sudo().write({'number_next': 1})
            else:
                # Altrimenti, verifica se la pratica che stai eliminando è l'ultima nella sequenza
                last_pratica = self.search([], order='name desc', limit=1)
                if last_pratica and any(record.name == last_pratica.name for record in self):
                    sequence.sudo().write({'number_next': sequence.number_next - len(self)})
        return super(HospitalAccreditation, self).unlink()

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
        return True

    def action_refuse(self):
        self.write({'state': 'refused'})
        for record in self:
            if record.struttura_da_accreditare_id:
                record.struttura_da_accreditare_id.write({
                    'e_accreditata': False
                })
        return True

    def action_forward(self):
        self.write({'state': 'to_be_approved'})
        return True

    def action_backward(self):
        self.write({'state': 'draft'})
        return True


    
#FIX DA FARE
# 1) Gestione dei duplicate: in particolare, quando premo Duplicate, la pratica, nel tornare allo stato "In compilazione", deve avere i seguenti records già compilati:
# richiedente, codice pratica e autore registrazione: quelli da compilarsi devono essere solo la descrizione, la Struttura sanitaria ed il nome della pratica deve avanzare di uno grazie all'utilizzo
# di un ir_sequence_data.xml
# 2) Elimininazione del flag "è una struttura sanitaria" dalla lista delle "Strutture Sanitarie"
# 3) ripristinare ir_sequence_data.xml

    





