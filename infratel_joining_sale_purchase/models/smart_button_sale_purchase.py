from odoo import models, fields, api

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
