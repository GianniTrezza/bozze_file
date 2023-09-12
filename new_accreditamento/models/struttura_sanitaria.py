from odoo import models, fields

class StrutturaSanitaria(models.Model):
    _inherit = 'res.partner'

    is_company = fields.Boolean("Nome Struttura", default=True)
    is_struttura_sanitaria = fields.Boolean('È una struttura sanitaria', default=True)
    e_accreditata = fields.Boolean('Accreditata', default=True)



    # @api.onchange("is_company")
    # def _onchange_is_company(self):
    #     if self.is_company:
    #         self.is_struttura_sanitaria=True
    #     else:
    #         self.is_struttura_sanitaria=False

    # @api.onchange('is_struttura_sanitaria')
    # def onchange_is_struttura_sanitaria(self):
    #     if self.is_struttura_sanitaria:
    #         self.is_company = True

