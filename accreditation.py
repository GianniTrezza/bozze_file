from odoo import models, api, fields, _
from odoo.exceptions import UserError

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
    def _compute_state_selection(self):
        is_manager = self.user_has_groups('new_accreditamento.group_hospital_accreditation_manager')
        if is_manager:
            return [
                ('draft', 'In Compilazione'),
                ('to_be_approved', 'Da Approvare'),
                ('approved', 'Approvato'),
                ('refused', 'Rifiutato'),
            ]
        else:
            return [('draft', 'In Compilazione')]

    state = fields.Selection(selection='_compute_state_selection', default='draft', readonly=True, track_visibility='onchange')
    
    mode = fields.Selection([
        ('user', 'User'),
        ('manager', 'Manager')
    ], default='user', string='Modalità')

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
        struttura_ids_to_check = []        
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
                self.env['res.partner'].browse(struttura_id).write({'e_accreditata': False})
        return result

    def action_recorded(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_user'):
            raise UserError(_("Solo gli utenti possono registrare la pratica."))
        self.write({'state': 'draft'})

    def action_to_be_approved(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_user'):
            raise UserError(_("Solo gli utenti possono mandare la pratica in approvazione."))
        self.write({'state': 'to_be_approved'})
    def action_approve(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_manager'):
            raise UserError(_("Solo i manager possono approvare la pratica."))
        self.write({
            'state': 'approved',
            'acc_number': self.env['ir.sequence'].next_by_code('hospital.accreditation.accnumber'),
        })
        self.struttura_da_accreditare_id.write({'e_accreditata': True})
        body_approved = _("La tua pratica %s è stata approvata.") % (self.name)
        self._notify_user_thread(body_approved)

    def action_refuse(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_manager'):
            raise UserError(_("Solo i manager possono rifiutare la pratica."))
        self.write({'state': 'refused'})
        body_refused = _("La tua pratica %s è stata rifiutata.") % (self.name)
        self._notify_user_thread(body_refused)

    def action_reset_to_draft(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_manager'):
            raise UserError(_("Solo i manager possono reimpostare la pratica su 'In Compilazione'."))
        self.write({'state': 'draft'})
    def action_forward(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_manager'):
            raise UserError(_("Solo i manager possono avanzare la pratica."))
        self.write({'state': 'to_be_approved'})

    def action_backward(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_manager'):
            raise UserError(_("Solo i manager possono riportare la pratica allo stato precedente."))
        self.write({'state': 'draft'})

    def print_report(self):
        if not self.user_has_groups('new_accreditamento.group_hospital_accreditation_manager'):
            raise UserError(_("Solo i manager possono stampare il report: capitoH??!!!!??"))
        if self.state != 'approved':
            raise UserError(_("Solo le pratiche approvate possono essere stampate."))


    def _notify_user_thread(self, body):
        for record in self:
            if record.autore_reg_id:
                record.message_post(body=body, partner_ids=[record.autore_reg_id.partner_id.id])

    def _notify_manager_thread(self, body):
        manager_group = self.env.ref('new_accreditamento.group_hospital_accreditation_manager')
        for record in self:
            partner_ids = [user.partner_id.id for user in manager_group.users]
            record.message_post(body=body, partner_ids=partner_ids)

    


# PARTI COMMENTATE:
# 1) BOTTONE REFUSE:
# Nuova bottone refuse utilizzabile solo dal manager
    # def action_refuse(self):
    #     body = "La tua pratica è stata rifiutata e necessita di ulteriori integrazioni."
    #     self.write({'state': 'refused'})
    #     self._notify_user(body)
    #     for record in self:
    #         if record.struttura_da_accreditare_id:
    #             record.struttura_da_accreditare_id.write({
    #                 'e_accreditata': False
    #             })
    #     return True
#Vecchio bottone del refuse
    # def action_refuse(self):
    #     self.write({'state': 'refused'})
    #     for record in self:
    #         if record.struttura_da_accreditare_id:
    #             record.struttura_da_accreditare_id.write({
    #                 'e_accreditata': False
    #             })
    #     return True

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

#2) NUOVE FIX RICHIESTE DA RAFFAELE: SEPARAZIONE TRA USER E MANAGER: INIZIO
    # def _notify_user(self, body):
    #     template = self.env.ref('new_accreditamento.email_template_notify_user')
    #     for record in self:
    #         self.env['mail.mail'].create({
    #             'subject': 'Notifica Pratica',
    #             'body_html': body,
    #             'recipient_ids': [(4, record.autore_reg_id.partner_id.id)]
    #         }).send()

    # def _notify_manager(self, body):
    #     manager = self.env.user.partner_id
    #     self.env['mail.mail'].create({
    #         'subject': 'Notifica Pratica',
    #         'body_html': body,
    #         'recipient_ids': [(4, manager.id)]
    #     }).send()

    





