# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import api, fields, models 

class FrameworkAgreement(models.Model):
    _inherit = 'framework.agreement'

    product_ids = fields.Many2many('product.template', string="Prodotti")