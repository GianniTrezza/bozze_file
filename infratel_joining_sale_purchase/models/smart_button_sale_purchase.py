# from odoo import models, fields, api
# from odoo.exceptions import UserError

# class SaleOrder(models.Model):
#     _inherit = "sale.order"
    

#     related_purchase_order_id = fields.Many2one(
#         'purchase.order', string='Ordine di Acquisto Correlato',
#         readonly=True, ondelete='set null'
#     )
    
#     display_purchase_order_button = fields.Boolean(compute='_compute_display_purchase_order_button')
   
#     @api.depends('related_purchase_order_id')
#     def _compute_display_purchase_order_button(self):
#         for order in self:
#             order.display_purchase_order_button = bool(order.related_purchase_order_id)
#     def create_corresponding_purchase_order(self):
#         # Ricerca un fornitore che soddisfi il criterio specificato nel campo 'fornitore_id'
#         fornitore = self.env['res.partner'].search([('infr_contact_type', '=', 'fornitore')], limit=1)
#         if not fornitore:
#             # Gestisci il caso in cui non viene trovato alcun fornitore
#             raise UserError("Nessun fornitore trovato con il tipo di contatto 'fornitore'.")

#         purchase_order = self.env['purchase.order'].create({
#             'partner_id': fornitore.id,  # Imposta il fornitore qui
#             'related_sale_order_id': self.id,
#             # ... altri campi necessari per creare un ordine di acquisto ...
#         })
#         self.related_purchase_order_id = purchase_order.id

#     def write(self, vals):
#         # Override del metodo write per gestire la creazione dell'ODA
#         res = super(SaleOrder, self).write(vals)
#         if 'state' in vals and vals['state'] == 'sale':
#             self.create_corresponding_purchase_order()
#         return res
#     def link_purchase_order(self, purchase_order_id):
#         self.related_purchase_order_id = purchase_order_id

#     def action_view_related_purchase_order(self):
#         self.ensure_one()
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Ordine di Acquisto Correlato',
#             'res_model': 'purchase.order',
#             'view_mode': 'form',
#             'res_id': self.related_purchase_order_id.id,
#             'target': 'current',
#         }

# class PurchaseOrder(models.Model):
#     _inherit = "purchase.order"

#     related_sale_order_id = fields.Many2one(
#         'sale.order', string='Ordine di Vendita Correlato',
#         readonly=True, ondelete='set null'
#     )

#     display_sale_order_button = fields.Boolean(compute='_compute_display_sale_order_button')

#     @api.depends('related_sale_order_id')
#     def _compute_display_sale_order_button(self):
#         for order in self:
#             order.display_sale_order_button = bool(order.related_sale_order_id)

#     def action_view_related_sale_order(self):

        
#         self.ensure_one()
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Ordine di Vendita Correlato',
#             'res_model': 'sale.order',
#             'view_mode': 'form',
#             'res_id': self.related_sale_order_id.id,
#             'target': 'current',
#         }

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    related_purchase_order_id = fields.Many2one(
        'purchase.order', string='Ordine di Acquisto Correlato',
        readonly=True, ondelete='set null'
    )
    
    display_purchase_order_button = fields.Boolean(compute='_compute_display_purchase_order_button')
   
    @api.depends('related_purchase_order_id')
    def _compute_display_purchase_order_button(self):
        for order in self:
            order.display_purchase_order_button = bool(order.related_purchase_order_id)

    def action_view_related_purchase_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ordine di Acquisto Correlato',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': self.related_purchase_order_id.id,
            'target': 'current',
        }

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    related_sale_order_id = fields.Many2one(
        'sale.order', string='Ordine di Vendita Correlato',
        readonly=True, ondelete='set null'
    )

    display_sale_order_button = fields.Boolean(compute='_compute_display_sale_order_button')

    @api.depends('related_sale_order_id')
    def _compute_display_sale_order_button(self):
        for order in self:
            order.display_sale_order_button = bool(order.related_sale_order_id)

    

    def action_view_related_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ordine di Vendita Correlato',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.related_sale_order_id.id,
            'target': 'current',
        }
