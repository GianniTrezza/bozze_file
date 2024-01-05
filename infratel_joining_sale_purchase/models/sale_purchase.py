from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

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
            'context': {'default_sale_order_id': self.id},
        }

class FornitoreWizard(models.TransientModel):
    _name = 'fornitori.wizard'
    _description = 'Selezione di un fornitore e dei prodotti per l\'ODA'

    fornitore_id = fields.Many2one('res.partner', string='Fornitore', domain=[('infr_contact_type', '=', 'fornitore')])
    accordo_quadro_id = fields.Many2one('framework.agreement', string='Accordi Quadro Attivi', domain="[('partner_id', '=', fornitore_id), ('is_state_valid', '=', True)]")
    available_product_ids = fields.Many2many('product.product', compute='_compute_available_product_ids', string='Prodotti Disponibili')
    product_ids = fields.Many2many('product.product', string='Prodotti Selezionati', domain="[('id', 'in', available_product_ids)]", options={'no_create': True})

    @api.depends('fornitore_id')
    def _compute_available_product_ids(self):
        for record in self:
            sale_order_id = self.env.context.get('default_sale_order_id')
            _logger.info(f"Sale order ID: {sale_order_id}")

            if sale_order_id:
                sale_order = self.env['sale.order'].browse(sale_order_id)
                product_ids = sale_order.order_line.mapped('product_id').filtered(lambda p: p.purchase_ok).ids
                _logger.info(f"Product IDs: {product_ids}")

                record.available_product_ids = [(6, 0, product_ids)]
            else:
                record.available_product_ids = [(6, 0, [])]

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
            'res_model': 'fornitori.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_partner_id': self.fornitore_id.id,
                        'default_sale_order_id': self.env.context.get('default_sale_order_id')}
        }

    def conferma_selezione_prodotti(self):
        self.ensure_one()
        partner_id = self.fornitore_id.id
        
        if not self.product_ids:
            raise UserError('Scegli almeno un prodotto oppure verifica che la selezione dei prodotti sia attiva e funzionante.')
        if not partner_id:
            raise UserError('ID del fornitore non trovato nel contesto.')
        
        purchase_order = self.env['purchase.order'].create({
            'partner_id': partner_id,
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

#**********************Filtraggio dei soli prodotti presenti nell'ODV e che possono essere venduti*****************
# class ListaProdotti(models.TransientModel):
#     _name = 'prodotti.lista'
#     _description = 'Selezione dei prodotti per l\'ODA'

#     available_product_ids = fields.Many2many('product.product', compute='_compute_available_product_ids', string='Prodotti Disponibili')
#     product_ids = fields.Many2many('product.product', string='Prodotti Selezionati', domain="[('id', 'in', available_product_ids)]")


#     fornitore_id = fields.Many2one('res.partner', string='Fornitore', domain=[('infr_contact_type', '=', 'fornitore')])
# # FUNZIONE FILTRANTE I PRODOTTI SULLA BASE DEL FATTO CHE SIANO PRESENTI NELL'ODV E SULLA BASE DEL FATTO CHE SIANO VENDIBILI
#     @api.depends('fornitore_id')
#     def _compute_available_product_ids(self):
#         for record in self:
#             sale_order_id = self.env.context.get('default_sale_order_id')
#             _logger.info(f"Sale order ID: {sale_order_id}")

#             if sale_order_id:
#                 sale_order = self.env['sale.order'].browse(sale_order_id)
#                 # product_ids = sale_order.order_line.mapped('product_id').filtered(lambda p: p.purchase_ok).ids
#                 product_ids = sale_order.order_line.mapped('product_id').filtered(lambda p: p.purchase_ok).ids
#                 _logger.info(f"Product IDs: {product_ids}")

#                 record.available_product_ids = [(6, 0, product_ids)]
#             else:
#                 record.available_product_ids = [(6, 0, [])]
#     @api.model
#     def default_get(self, fields):
#         res = super(ListaProdotti, self).default_get(fields)
#         sale_order_id = self.env.context.get('default_sale_order_id')
#         if sale_order_id:
#             sale_order = self.env['sale.order'].browse(sale_order_id)
#             product_ids = sale_order.order_line.mapped('product_id').filtered(lambda p: p.purchase_ok).ids
#             res['available_product_ids'] = [(6, 0, product_ids)]
#         return res

#     def conferma_selezione_prodotti(self):
#         self.ensure_one()
#         if not self.product_ids:
#             raise UserError('Scegli almeno un prodotto oppure verifica che la selezione dei prodotti sia attiva e funzionante.')
#         if not self.env.context.get('default_partner_id'):
#             raise UserError('ID del fornitore non trovato nel contesto.')
        
#         purchase_order = self.env['purchase.order'].create({
#             'partner_id': self.env.context['default_partner_id'],
#             'origin': self._context.get('origin'),
#             'project_request_id': self._context.get('project_request_id'),
#             'infr_order': self._context.get('infr_order'),
#             'framework_agreement_id': self._context.get('framework_agreement_id')

#         })

#         for product in self.product_ids:
#             self.env['purchase.order.line'].create({
#                 'order_id': purchase_order.id,
#                 'product_id': product.id,
#                 'date_planned': fields.Datetime.now(),
#             })

#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Ordine di Acquisto Creato',
#             'res_model': 'purchase.order',
#             'res_id': purchase_order.id,
#             'view_mode': 'form',
#         }
    
# infratel_joining_sale_purchase.access_prodotti_lista,access_prodotti_lista,infratel_joining_sale_purchase.model_prodotti_lista,base.group_user,1,1,1,1
