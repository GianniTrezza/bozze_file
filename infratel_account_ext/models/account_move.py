# Copyright 2023 Raffaele Amalfitano, Unitiva

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"
    
    # only for customer invoices
    is_quadrature_possible = fields.Boolean(string="Quadratura Possibile")
    
    def trasmission_action(self):
        # Logica associata all'azione di "Invia per trasmissione"
        # Puoi implementare qui la logica desiderata quando l'utente fa clic sul pulsante "Invia per trasmissione"
        return True

    def sap_action(self):
        # Logica associata all'azione di "Invia a SAP"
        # Puoi implementare qui la logica desiderata quando l'utente fa clic sul pulsante "Invia a SAP"
        return True

    def create_penalties_action(self):
        # Logica associata all'azione di "Genera penale"
        # Puoi implementare qui la logica desiderata quando l'utente fa clic sul pulsante "Genera penale"
        return True


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    plant_route_id = fields.Many2one('plant.route', string="Tratta")
    route_length_rel = fields.Char(related='plant_route_id.route_length', string="Lunghezza tratta")
    iru_duration_id = fields.Many2one('iru.duration', string="Durata IRU")
    registered_goods_receipt = fields.Boolean(string="Entrata merci registrata")
    goods_receipt_code = fields.Boolean(string="Codice entrata merci")
    goods_receipt_validity = fields.Date(string="Validità entrata merci")