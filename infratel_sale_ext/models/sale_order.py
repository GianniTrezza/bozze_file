# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_request_id = fields.Many2one('project.request', string="Progetto relativo a")
    infr_order = fields.Char(string="Commessa")
    framework_agreement_id = fields.Many2one('framework.agreement', string="Accordo quadro",
        help="""Accordo quadro legato al cliente dell'ordine di vendita""")
    filtered_framework_agreement_ids = fields.Many2many('framework.agreement',
        compute='_compute_filtered_framework_agreement_ids')
    cig = fields.Char(string="CIG")
    cup = fields.Char(string="CUP")
    request_type = fields.Selection([
        ('backhualing', 'Backhualing'),
        ('access_network', 'Rete di accesso')
        ], string="Tipo richiesta")

    # contact referent data
    contact_referent_id = fields.Many2one('res.partner', string="Referente",
        help="""Contatto operatore, figlio del contatto 'Cliente'.""")
    email_rel = fields.Char(related='contact_referent_id.email', string="E-mail")
    pec_rel = fields.Char(related='contact_referent_id.email_pec', string="E-mail PEC")
    phone_rel = fields.Char(related='contact_referent_id.phone', string="Telefono")

    joint_testing = fields.Boolean(string="Collaudo congiunto")
    is_quadrature_possible = fields.Boolean(string="Quadratura possibile")
    
    # users related to specific groups
    business_developer_id = fields.Many2one('res.users', string="Business Developer")
    delivery_employee_id = fields.Many2one('res.users',  string="Dipendente delivery")

    def _compute_filtered_framework_agreement_ids(self):
        """
        Retrieve valid agreements related to the
        sale order 'partner_id' field
        """
        for r in self:
            if r.partner_id and r.partner_id.framework_agreement_ids:
                r.filtered_framework_agreement_ids = [(6, 0, r.partner_id.framework_agreement_ids.filtered(lambda x: x.state == 'valid').ids)]
            else:
                r.filtered_framework_agreement_ids = False
    
    def validation_action(self):
        return True

    def approval_action(self):
        return True

    def signature_action(self):
        return True

    def information_action(self):
        return True

    def create_purchase_order_action(self):
        if self.state != 'sale':
            raise UserError("L'ODV deve essere confermato per generare un ODA.")
        if not self.partner_id:
            raise UserError("Devi selezionare un cliente prima di creare un ordine di acquisto.")
        _logger.info(f"Creazione ODA per Sale Order {self.name} con partner_id: {self.partner_id.id}")


        partner = self.env['res.partner'].browse(self.partner_id.id)
        if not partner.exists():
            raise UserError("Fornitore non valido o non esistente per l'ODV.")

        return {
            'name': 'Seleziona Fornitore',
            'type': 'ir.actions.act_window',
            'res_model': 'fornitori.wizard',  
            'view_mode': 'form',
            'target': 'new',
            'context': {
            },
        }

    def renewal_action(self):
        return True

    def divestment_action(self):
        return True   


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    plant_route_id = fields.Many2one('plant.route', string="Tratta")
    route_length_rel = fields.Char(related='plant_route_id.route_length', string="Lunghezza tratta")
    iru_duration_id = fields.Many2one('iru.duration', string="Durata IRU")

# ***********************GENERAZIONE DEL WIZARD LEGATO AL TASTO "CREAZIONE ODA" (SVILUPPO)****************************
#*******************Filtraggio dei soli fornitori e degli accordi quadro ancora attivi ad essi correlati***********************
class FornitoreWizard(models.TransientModel):
    _name = 'fornitori.wizard'
    _description = 'Selezione di un fornitore per l\'ODA'

    fornitore_id = fields.Many2one('res.partner', string='Fornitore', domain=[('infr_contact_type', '=', 'fornitore')])
    accordo_quadro_id = fields.Many2one('framework.agreement', string='Accordi Quadro Attivi', domain="[('partner_id', '=', fornitore_id), ('is_state_valid', '=', True)]")
    
    def conferma_selezione_accordo_quadro(self):
        self.ensure_one()
        if not self.accordo_quadro_id:
            raise UserError('Seleziona un accordo quadro.')
        if not self.fornitore_id:
            raise UserError('Seleziona un fornitore prima di procedere.')

        _logger.info(f"Fornitore selezionato ID: {self.fornitore_id.id}")
        
        return {
            'name': 'Seleziona Prodotti',
            'type': 'ir.actions.act_window',
            'res_model': 'prodotti.lista',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_partner_id': self.fornitore_id.id},
        }
#**********************Filtraggio dei soli fornitori e degli accordi quadro ancora attivi ad essi correlati*****************
class ListaProdotti(models.TransientModel):
    _name = 'prodotti.lista'
    _description = 'Selezione dei prodotti per l\'ODA'
    
    product_ids = fields.Many2many('product.product', string='Prodotti disponibili')
    fornitore_id = fields.Many2one('res.partner', string='Fornitore', domain=[('infr_contact_type', '=', 'fornitore')])
    
    def conferma_selezione_prodotti(self):
        self.ensure_one()
        if not self.product_ids:
            raise UserError('Scegli almeno un prodotto.')
        if not self.env.context.get('default_partner_id'):
            raise UserError('ID del fornitore non trovato nel contesto.')
        
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.env.context['default_partner_id'],
            'origin': self._context.get('origin'),
            'project_request_id': self._context.get('project_request_id'),
            'infr_order': self._context.get('infr_order'),
            'framework_agreement_id': self._context.get('framework_agreement_id')

        })
        for product in self.product_ids:
            self.env['purchase.order.line'].create({
                'order_id': purchase_order.id,
                'product_id': product.id,
                'date_planned': fields.Datetime.now(),
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Ordine di Acquisto Creato',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
        }
