# PRIMO TENTATIVO:Vecchio codice

# from odoo import api, fields, models, _
# import base64
# import csv
# from io import StringIO

# class TabellaFatture(models.Model):
#     _name = 'tabella.fatture'
#     _description = 'Tabella Fatture di Unitiva'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _order = "data_fattura desc"

#     cliente_id = fields.Char(string='ID Cliente', readonly=True, copy=False, default=lambda self: _('New'))
#     data_fattura = fields.Date(string="Data fattura")
#     numero = fields.Char(string="Numero")
#     addetto_vendite = fields.Char(string="Addetto vendite")
#     data_scadenza = fields.Date(string="Data scadenza")
#     documento_origine = fields.Char(string="Documento origine")
#     insoluta = fields.Boolean(string="Insoluta")
#     imponibile = fields.Float(string="Imponibile")
#     imposta = fields.Float(string="Imposta")
#     totale = fields.Float(string="Totale")
#     importo_dovuto = fields.Float(string="Importo dovuto")
#     stato_efattura = fields.Selection([
#         ('draft', 'Bozza'),
#         ('open', 'Aperta'),
#         ('paid', 'Pagata'),
#         ('cancelled', 'Annullata')
#     ], string="Stato e-fattura")
#     # stato = fields.Selection([
#     #     ('draft', 'Bozza'),
#     #     ('recorded', 'Registrato'),
#     #     ('approved', 'Approvato')
#     # ], string="Stato", default='draft')

#     @api.model
#     def create(self, vals):
#         if vals.get('cliente_id'):
#             vals['cliente_id'] = self.env['ir.sequence'].next_by_code('tabella.fatture')
#         return super(TabellaFatture, self).create(vals)

# class TabellaFattureImportWizard(models.TransientModel):
#     _name = 'tabella.fatture.import.wizard'
    
#     data_file = fields.Binary(string='CSV File', required=True)
#     filename = fields.Char(string='Filename')

#     def _generate_client_ids(self, csv_data):
#         clients = set(row[0] for row in csv_data)
#         return {client: str(i).zfill(6) for i, client in enumerate(clients, 1)}

#     def _generate_salesperson_ids(self, csv_data):
#         salespeople = set(row[3] for row in csv_data)
#         return {salesperson: f"addetto_{i}" for i, salesperson in enumerate(salespeople, 1)}

#     def button_import(self):
#         self.ensure_one()
        
#         file_data = base64.b64decode(self.data_file)
#         file_input = StringIO(file_data.decode('utf-8'))
#         csv_file = list(csv.reader(file_input, delimiter=',', lineterminator='\n'))

#         client_ids = self._generate_client_ids(csv_file[1:])
#         salesperson_ids = self._generate_salesperson_ids(csv_file[1:])

#         for row in csv_file[1:]:
#             salesperson_id = salesperson_ids[row[3].strip()]

#             values = {
#                 'cliente_id': client_ids[row[0]],
#                 'data_fattura': row[1],
#                 'numero': row[2],
#                 'addetto_vendite': salesperson_id,
#                 'data_scadenza': row[4],
#                 'documento_origine': row[5],
#                 'insoluta': True if row[6] == 'Insoluta' else False,
#                 'imponibile': float(row[7]),
#                 'imposta': float(row[8]),
#                 'totale': float(row[9]),
#                 'importo_dovuto': float(row[10]),
#                 'stato_efattura': 'open' if row[11] == 'Aperta' else ('paid' if row[11] == 'Pagata' else 'draft')
#             }
#             self.env['tabella.fatture'].create(values)

#         return {'type': 'ir.actions.act_window_close'}

#SECONDO TENTATIVO: Questo codice mi dà la possobilità di generare il pulsante import_file, ma non riesce a caricare il file
# import csv
# import os
# import base64
# from io import StringIO
# from odoo import api, fields, models, _

# class TabellaFatture(models.Model):
#     _name = 'tabella.fatture'
#     _description = 'Tabella Fatture di Unitiva'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _order = "data_fattura desc"

#     cliente_id = fields.Char(string='ID Cliente', readonly=True, copy=False, default=lambda self: _('New'))
#     data_fattura = fields.Date(string="Data fattura")
#     numero = fields.Char(string="Numero")
#     addetto_vendite = fields.Char(string="Addetto vendite")
#     data_scadenza = fields.Date(string="Data scadenza")
#     documento_origine = fields.Char(string="Documento origine")
#     insoluta = fields.Boolean(string="Insoluta")
#     imponibile = fields.Float(string="Imponibile")
#     imposta = fields.Float(string="Imposta")
#     totale = fields.Float(string="Totale")
#     importo_dovuto = fields.Float(string="Importo dovuto")
#     stato_efattura = fields.Selection([('draft', 'Bozza'), ('open', 'Aperta'), ('paid', 'Pagata'), ('cancelled', 'Annullata')], string="Stato e-fattura")

#     @api.model
#     def load_from_csv(self):
#         path = os.path.expanduser("C:/Users/giova/OneDrive/Desktop/tabella_fatture.csv")

#         with open(path, 'r', encoding='utf-8-sig') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 self.create({
#                     'cliente_id': row['ID Cliente'],
#                     'data_fattura': row['Data fattura'],
#                     'numero': row['Numero'],
#                     'addetto_vendite': row['Addetto vendite'],
#                     'data_scadenza': row['Data scadenza'],
#                     'documento_origine': row['Documento origine'],
#                     'insoluta': True if row['Insoluta'] == 'Si' else False,
#                     'imponibile': float(row['Imponibile']),
#                     'imposta': float(row['Imposta']),
#                     'totale': float(row['Totale']),
#                     'importo_dovuto': float(row['Importo dovuto']),
#                     'stato_efattura': row['Stato e Fattura']
#                     # 'stato': row['Stato']
#                 })

#     @api.model
#     def create(self, vals):
#         if vals.get('cliente_id', _('New')) == _('New'):
#             vals['cliente_id'] = self.env['ir.sequence'].next_by_code('tabella.fatture.sequence')
#         return super(TabellaFatture, self).create(vals)
    
#     data_file = fields.Binary(string='CSV File', required=True)
#     filename = fields.Char(string='Filename')

#     def _generate_client_ids(self, csv_data):
#         clients = set(row[0] for row in csv_data)
#         return {client: str(i).zfill(6) for i, client in enumerate(clients, 1)}

#     def _generate_salesperson_ids(self, csv_data):
#         salespeople = set(row[3] for row in csv_data)
#         return {salesperson: f"addetto_{i}" for i, salesperson in enumerate(salespeople, 1)}

#     def button_import(self):

#         self.ensure_one()
#         file_data = base64.b64decode(self.data_file)
#         file_input = StringIO(file_data.decode('utf-8'))
#         csv_file = list(csv.reader(file_input, delimiter=',', lineterminator='\n'))

#         client_ids = self._generate_client_ids(csv_file[1:])
#         salesperson_ids = self._generate_salesperson_ids(csv_file[1:])

#         for row in csv_file[1:]:

#                 salesperson_id = salesperson_ids.get(row[3].strip(), False)
#                 if not salesperson_id:
                    
#                     continue  

#                 values = {
#                     'cliente_id': client_ids[row[0]],
#                     'data_fattura': row[1],
#                     'numero': row[2],
#                     'addetto_vendite': salesperson_id,
#                     'data_scadenza': row[4],
#                     'documento_origine': row[5],
#                     'insoluta': True if row[6] == 'Insoluta' else False,
#                     'imponibile': float(row[7]),
#                     'imposta': float(row[8]),
#                     'totale': float(row[9]),
#                     'importo_dovuto': float(row[10]),
#                     'stato_efattura': 'open' if row[11] == 'Aperta' else ('paid' if row[11] == 'Pagata' else 'draft')
#                 }
#                 self.env['tabella.fatture'].create(values)

        # return {'type': 'ir.actions.act_window'}
import csv
import os
import base64
from io import StringIO
from odoo import api, fields, models, _
# from odoo.exceptions import UserError
from datetime import datetime

def convert_date_format(original_date):
    try:
        formatted_date = datetime.strptime(original_date.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {original_date}")
    return formatted_date


class TabellaFatture(models.Model):
    _name = 'tabella.fatture'
    _description = 'Tabella Fatture di Unitiva'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "data_fattura desc"
    _order = "numero desc"

    cliente_id = fields.Char(string='ID Cliente', copy=False, default=lambda self: _('New'))
    data_fattura = fields.Date(string="Data fattura")
    numero = fields.Char(string="Numero")
    addetto_vendite = fields.Char(string="Addetto vendite")
    data_scadenza = fields.Date(string="Data scadenza")
    documento_origine = fields.Char(string="Documento origine")
    insoluta = fields.Boolean(string="Insoluta")
    imponibile = fields.Float(string="Imponibile")
    imposta = fields.Float(string="Imposta")
    totale = fields.Float(string="Totale")
    importo_dovuto = fields.Float(string="Importo dovuto")

    stato_efattura = fields.Selection([('draft', 'Bozza'), ('open', 'Aperta'), ('paid', 'Pagata'), ('cancelled', 'Annullata')], string="Stato e-fattura")
    data_file = fields.Binary(string='CSV File', required=True)
    filename = fields.Char(string='Filename')

    @api.model
    def create(self, vals):
        if vals.get('cliente_id', _('New')) == _('New'):
            vals['cliente_id'] = self.env['ir.sequence'].next_by_code('tabella.fatture.sequence')
        return super(TabellaFatture, self).create(vals)

    def _generate_client_ids(self, csv_data):
        clients = set(row[0] for row in csv_data)
        return {client: str(i).zfill(6) for i, client in enumerate(clients, 1)}

    def _generate_salesperson_ids(self, csv_data):
        salespeople = set(row[3] for row in csv_data)
        return {salesperson: f"addetto_{i}" for i, salesperson in enumerate(salespeople, 1)}

    def button_import(self):
        # try:
        file_data = base64.b64decode(self.data_file)
        file_input = StringIO(file_data.decode('utf-8'))
        csv_file = list(csv.reader(file_input, delimiter=',', lineterminator='\n'))

        client_ids = self._generate_client_ids(csv_file[1:])
        salesperson_ids = self._generate_salesperson_ids(csv_file[1:])

        for row in csv_file[1:]:
            salesperson_id = salesperson_ids.get(row[3].strip())
            # if not salesperson_id:
            #     raise UserError(_('Addetto vendite non trovato: %s') % row[3].strip())
            values = {
                'cliente_id': client_ids[row[0]],
                'data_fattura': convert_date_format(row[1]),
                'numero': row[2],
                'addetto_vendite': salesperson_id,
                'data_scadenza': convert_date_format(row[4]),
                'documento_origine': row[5],
                'insoluta': True if row[6] == 'Insoluta' else False,
                'imponibile': float(row[7]) if row[7] else 0.0,
                'imposta': float(row[8]) if row[8] else 0.0,
                'totale': float(row[9]) if row[9] else 0.0,
                'importo_dovuto': float(row[10]) if row[10] else 0.0,
                'stato_efattura':'open' if row[11] == 'Aperta' else ('paid' if row[11] == 'Pagata' else 'draft')
            }
            self.env['tabella.fatture'].create(values)


        # except Exception as e:
        #     raise UserError(_('Errore durante l\'importazione: %s') % str(e))




    # @api.model
    # def create(self, vals):
    #     global clienti_mapping

    #     cliente_id = vals.get('cliente_id')
        
    #     # Se abbiamo un cliente_id nella mappa, utilizziamo quello, altrimenti impostiamo a None.
    #     if cliente_id:
    #         if cliente_id not in clienti_mapping:
    #             clienti_mapping[cliente_id] = None
    #         vals['cliente_id'] = clienti_mapping.get(cliente_id)
    #     else:
    #         vals['cliente_id'] = None
        
    #     return super(TabellaFatture, self).create(vals)


    
# class TabellaFattureImportWizard(models.TransientModel):
#     _name = 'tabella.fatture.import.wizard'

#     data_file = fields.Binary(string='CSV File', required=True)
#     filename = fields.Char(string='Filename')

#     def _generate_client_ids(self, csv_data):
#         clients = set(row[0] for row in csv_data)
#         return {client: str(i).zfill(6) for i, client in enumerate(clients, 1)}

#     def _generate_salesperson_ids(self, csv_data):
#         salespeople = set(row[3] for row in csv_data)
#         return {salesperson: f"addetto_{i}" for i, salesperson in enumerate(salespeople, 1)}

#     def button_import(self):
#         self.ensure_one()
#         file_data = base64.b64decode(self.data_file)
#         file_input = StringIO(file_data.decode('utf-8'))
#         csv_file = list(csv.reader(file_input, delimiter=',', lineterminator='\n'))

#         client_ids = self._generate_client_ids(csv_file[1:])
#         salesperson_ids = self._generate_salesperson_ids(csv_file[1:])

#         for row in csv_file[1:]:
#             salesperson_id = salesperson_ids[row[3].strip()]
#             values = {
#                 'cliente_id': client_ids[row[0]],
#                 'data_fattura': row[1],
#                 'numero': row[2],
#                 'addetto_vendite': salesperson_id,
#                 'data_scadenza': row[4],
#                 'documento_origine': row[5],
#                 'insoluta': True if row[6] == 'Insoluta' else False,
#                 'imponibile': float(row[7]),
#                 'imposta': float(row[8]),
#                 'totale': float(row[9]),
#                 'importo_dovuto': float(row[10]),
#                 'stato_efattura': 'open' if row[11] == 'Aperta' else ('paid' if row[11] == 'Pagata' else 'draft')
#             }
#             self.env['tabella.fatture'].create(values)
        # return {'type': 'ir.actions.act_window'}




  