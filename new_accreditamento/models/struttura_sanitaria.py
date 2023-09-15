from odoo import models, fields

class StrutturaSanitaria(models.Model):
    _inherit = 'res.partner'

    is_company = fields.Boolean("Nome Struttura", default=True)
    is_struttura_sanitaria = fields.Boolean('È una struttura sanitaria', default=False)
    e_accreditata = fields.Boolean('Accreditata', default=False)

