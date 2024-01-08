from odoo import models, fields, api
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    state = fields.Selection(selection_add=[
            ('sent_for_validation', 'In attesa di validazione'),
            ('sent_for_approval', 'In attesa di approvazione'),
            ('signed', 'Firmato')
        ])
    button_validation_visible = fields.Boolean(compute='_compute_button_visibility')
    button_approval_visible = fields.Boolean(compute='_compute_button_visibility')
    button_sign_visible = fields.Boolean(compute='_compute_button_visibility')

    # Logiche per la visibilità dei bottoni
    @api.depends('state', 'user_id')
    def _compute_button_visibility(self):
        for record in self:
            user = self.env.user
            # Qui inserisci la logica per definire se l'utente è un Business Developer o DDI
            is_business_developer = user.has_group('infratel_sale_bar_ext.group_business_developer_id')
            # is_ddi = user.has_group('your_module.group_ddi')

            record.button_validation_visible = record.state == 'draft'
            record.button_approval_visible = record.state == 'sent_for_validation' and is_business_developer
            record.button_sign_visible = record.state == 'sent_for_approval' 
            # Aggiungere a questo livello il is_ddi

    # Azione "Invia per validazione"
    def action_send_for_validation(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError("Il preventivo è in attesa d'approvazione da parte del Business Developer.")
        self.state = 'sent_for_validation'
        

    # Azione "Invia per approvazione"
    def action_send_for_approval(self):
        self.ensure_one()
        if self.state != 'sent_for_validation':
            raise UserError("Il preventivo è stato approvato: si attenda la firma e l'invio da parte del DDI.")
        self.state = 'sent_for_approval'

#***************************** Pulsante "Invia per approvazione" e stato "Firma"*************************

    def action_sign(self):
        # if self.state == 'sent_for_approval':
        #     self.state = 'signed'
        self.ensure_one()
        if self.state != 'sent_for_approval':
            raise UserError("Preventivo firmato ed inviato correttamente da parte del DDI.")
        self.write({'state': 'signed'})

# ********************************* ACCESSO UTENTI*************************************************
    # def is_user_business_developer(self):
    #     return self.env.user.has_group('infratel_sale_bar_ext.group_business_developer')
        
    # def is_user_ddi(self):
    #     return self.env.user.has_group('your_module.group_ddi')
            

# from odoo import models, fields, api

# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
    
#     state = fields.Selection(selection_add=[
#             ('sent_for_validation', 'In attesa di validazione'),
#             ('sent_for_approval', 'In attesa di approvazione'),
#             ('signed', 'Firmato')
#         ])
    
#     show_validation_button = fields.Boolean(compute='_compute_show_buttons')
#     show_approval_button = fields.Boolean(compute='_compute_show_buttons')
#     show_sign_button = fields.Boolean(compute='_compute_show_buttons')

#     @api.depends('state')
#     def _compute_show_buttons(self):
#         for record in self:
#             record.show_validation_button = record.state == 'draft'
#             record.show_approval_button = record.state == 'sent_for_validation'
#             record.show_sign_button = record.state == 'sent_for_approval'
    
#     def action_send_for_validation(self):
#         self.state = 'sent_for_validation'

#     def action_send_for_approval(self):
#         self.state = 'sent_for_approval'

#     def action_sign(self):
#         self.state = 'signed'



