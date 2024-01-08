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

    @api.depends('state', 'user_id')
    def _compute_button_visibility(self):
        for record in self:
            # user_in_group = self.env.user.has_group('infratel_sale_bar_ext.business_developer_id')
            # record.button_validation_visible = (record.state == 'draft')
            # record.button_approval_visible = (record.state == 'sent_for_validation')
            # record.button_sign_visible = (record.state == 'sent_for_approval')
            record.button_validation_visible = record.state == ['draft', 'sent_for_validation','sent_for_approval' ]
            record.button_approval_visible = record.state == ['sent_for_validation', 'sent_for_approval']
            record.button_sign_visible = record.state == 'sent_for_approval'

# *****************************Pulsante "Invia per validazione e stato "In attesa di validazione"********************************+

    
    def action_send_for_validation(self):
        # if self.state == 'draft':
        #     self.state = 'sent_for_validation'
        self.ensure_one()
        if self.state != 'draft':
            raise UserError("Il preventivo non è in stato bozza.")
        self.write({'state': 'sent_for_validation'})

#***************************** Pulsante "Invia per approvazione" e stato "In attesa di approvazione"*************************
    
    def action_send_for_approval(self):
        # if self.state == 'sent_for_validation':
        #     self.state = 'sent_for_approval'
        self.ensure_one()
        if self.state != 'sent_for_validation':
            raise UserError("Il preventivo non è in attesa di validazione.")
        self.write({'state': 'sent_for_approval'})

#***************************** Pulsante "Invia per approvazione" e stato "Firma"*************************

    def action_sign(self):
        # if self.state == 'sent_for_approval':
        #     self.state = 'signed'
        self.ensure_one()
        if self.state != 'sent_for_approval':
            raise UserError("Il preventivo non è in attesa di approvazione.")
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



