# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import  models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    available_portal_side = fields.Boolean(string="Disponibile lato portale")
    product_detail_type = fields.Selection([
        ('ricorrente', 'Ricorrente'),
        ('una_tantum', 'Una tantum')
        ], string="Dettaglio tipologia")
    