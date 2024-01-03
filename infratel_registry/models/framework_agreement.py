# Copyright 2023 Raffaele Amalfitano, Unitiva

from datetime import date
from odoo import api, exceptions, fields, models 

class FrameworkAgreement(models.Model):
    _name = 'framework.agreement'
    _description = "Framework agreement"

    name = fields.Char(string="Nome contratto", required=True)
    start_date = fields.Date(string="Data di inizio", required=True)
    end_date = fields.Date(string="Valido fino a", required=True)
    contract_attachment = fields.Binary(string="Contratto")
    day_alert = fields.Integer(string="Giorni alert", required=True)
    sla_policy_id = fields.Many2one('inf.sla.policy', string="Politica SLA", required=True)
    infratel_protocol = fields.Char(string="Protocollo Infratel", required=True)
    signing_date = fields.Date(string="Data di sottoscrizione", required=True)
    cig = fields.Char(string="CIG", required=True)
    state = fields.Selection([
        ('not_valid', 'Non valido'),
        ('valid', 'Valido'),
        ], string="Stato", default='not_valid', compute="_compute_state")
    is_state_valid = fields.Boolean(
        string="Stato Validità",
        compute="_compute_is_state_valid",
        store=True
    )
    # override 'create' method in order to manage
    # contract end date and state
    def _compute_state(self):
        for record in self:
            today = date.today()
            if record.start_date and record.start_date > today:
                record.state = 'not_valid'
            elif record.end_date and record.end_date < today:
                record.state = 'not_valid'
            else:
                record.state = 'valid'
    @api.depends('state')
    def _compute_is_state_valid(self):
        for record in self:
            record.is_state_valid = (record.state == 'valid')
    # def create(self, values):
    #     res = super(FrameworkAgreement, self).create(values)
    #     if res.end_date < date.today():
    #         res.state = 'not_valid'
    #     else:
    #         res.state = 'valid'
    #     return res

    # # override 'write' method in order to manage
    # # contract end date and state
    # def write(self, values):
    #     res = super(FrameworkAgreement, self).write(values)
    #     if 'end_date' in values:
    #         if self.end_date < date.today():
    #             self.state = 'not_valid'
    #         else:
    #             self.state = 'valid'
    #     return res


    @api.constrains('start_date', 'end_date')
    def _check_date_validity(self):
        for r in self:
            if r.start_date >= r.end_date:
                raise exceptions.ValidationError("Attenzione! 'Valido fino a' deve essere superiore a 'Data di inizio'!")

    # TO DO: serve fare un cron per controllare la data scadenza e la validità del contratto