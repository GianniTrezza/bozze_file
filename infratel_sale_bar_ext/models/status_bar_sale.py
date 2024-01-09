from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
        ('sent_for_validation', 'In attesa di validazione'),
        ('sent_for_approval', 'In attesa di approvazione'),
        ('signed', 'Firmato')
    ])

    # Campi calcolati per la visibilità dei pulsanti
    show_button_validation = fields.Boolean(compute='_compute_button_visibility')
    show_button_approval = fields.Boolean(compute='_compute_button_visibility')
    show_button_sign = fields.Boolean(compute='_compute_button_visibility')

    @api.depends('state')
    def _compute_button_visibility(self):
        for record in self:
            record.show_button_validation = record.state == 'draft'
            record.show_button_approval = record.state == 'sent_for_validation'
            record.show_button_sign = record.state == 'sent_for_approval'

    # Azione "Invia per validazione"
    def action_send_for_validation(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError("Il preventivo è in attesa di validazione da parte del Business Developer.")
        self.state = 'sent_for_validation'
        
    # Azione "Invia per approvazione"
    def action_send_for_approval(self):
        self.ensure_one()
        if self.state != 'sent_for_validation':
            raise UserError("Il preventivo è in attesa di approvazione da parte dell'utente DDI.")
        self.state = 'sent_for_approval'

    # Pulsante "Invia per approvazione" e stato "Firma"
    def action_sign(self):
        self.ensure_one()
        if self.state != 'sent_for_approval':
            raise UserError("Preventivo firmato correttamente da parte del DDI.")
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



