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
#Funzione sottostante per gestire il tasto DUPLICATE
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
#Funzione sottostante per gestire il tasto DELETE: inoltre, che gestisce anche la seguente casistica:
# Ho due pratiche legate alla stessa struttura sanitaria, di cui una approvata e l'altra rifiutata. 
# Sulla base del fatto che almeno una delle due è accettata, la struttura sanitaria è accreditata.
# Supponiamo, però, che io decida di eliminare una pratica approvata e che, quindi, resti solo quella rifiutata: 
# Questa logica fa sì che la struttura sanitaria resti tale, ma non sia più accreditata.
    def unlink(self):
        sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'hospital.accreditation.sequence')], limit=1)
        struttura_ids_to_check = []  # Lista delle strutture sanitarie da verificare dopo l'eliminazione

        
        for record in self:
            if record.state == 'approved' and record.struttura_da_accreditare_id:
                struttura_ids_to_check.append(record.struttura_da_accreditare_id.id)
        if sequence:
            record_count = self.search_count([])

            if record_count <= len(self):
                sequence.sudo().write({'number_next': 1})
            else:
                last_pratica = self.search([], order='name desc', limit=1)
                if last_pratica and any(record.name == last_pratica.name for record in self):
                    sequence.sudo().write({'number_next': sequence.number_next - len(self)})

        result = super(HospitalAccreditation, self).unlink()

        for struttura_id in struttura_ids_to_check:
            other_approved_pratiche = self.search([
                ('struttura_da_accreditare_id', '=', struttura_id),
                ('state', '=', 'approved')
            ])
            if not other_approved_pratiche: 
                struttura = self.env['res.partner'].browse(struttura_id)
                struttura.write({'e_accreditata': False})

        return result
# Questa funzione va bene, si comporta correttamente: ma voglio gestire la casistica legata alle strutture sanitarie, vista poc'anzi
    # def unlink(self):
    #     sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'hospital.accreditation.sequence')], limit=1)
    #     if sequence:
    #         record_count = self.search_count([])

    #         if record_count <= len(self):
    #             sequence.sudo().write({'number_next': 1})
    #         else:
    #             last_pratica = self.search([], order='name desc', limit=1)
    #             if last_pratica and any(record.name == last_pratica.name for record in self):
    #                 sequence.sudo().write({'number_next': sequence.number_next - len(self)})
    #     return super(HospitalAccreditation, self).unlink()

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



    





