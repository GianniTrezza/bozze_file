# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

#CODICE ORIGINALE
# import openai

# from odoo import api, fields, models, _
# from odoo.exceptions import UserError


# class Channel(models.Model):
#     _inherit = 'mail.channel'

#     def _notify_thread(self, message, msg_vals=False, **kwargs):
#         rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
#         chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
#         user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
#         partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
#         author_id = msg_vals.get('author_id')
#         chatgpt_name = str(partner_chatgpt.name or '') + ', '
#         prompt = msg_vals.get('body')
#         if not prompt:
#             return rdata
#         openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
#         Partner = self.env['res.partner']
#         partner_name = ''
#         if author_id:
#             partner_id = Partner.browse(author_id)
#             if partner_id:
#                 partner_name = partner_id.name
#         if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         return rdata

#     def _get_chatgpt_response(self, prompt):
#         ICP = self.env['ir.config_parameter'].sudo()
#         openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
#         gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
#         gpt_model = 'text-davinci-003'
#         try:
#             if gpt_model_id:
#                 gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
#         except Exception as ex:
#             gpt_model = 'text-davinci-003'
#             pass
#         try:
#             response = openai.Completion.create(
#                 model=gpt_model,
#                 prompt=prompt,
#                 temperature=0.6,
#                 max_tokens=3000,
#                 top_p=1,
#                 frequency_penalty=0,
#                 presence_penalty=0,
#                 user = self.env.user.name,
#             )
#             res = response['choices'][0]['text']
#             return res
#         except Exception as e:
#             raise UserError(_(e))

# CODICE FONDAMENTALE

#INIZIO CODICE FONDAMENTALE
# import pandas as pd
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# import io
# from PIL import Image
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# import openai
# import base64
# from odoo import api, fields, models
# from odoo.exceptions import UserError
# from odoo.tools.translate import _
# from datetime import datetime


# class Andamenti:
#     def __init__(self, file_path):
#         self.tabella = pd.read_csv(file_path, header=None,
#                                    names=["Cliente", "Data fattura", "Numero", "Addetto vendite", "Data scadenza",
#                                          "Documento origine", "Insoluta", "Imponibile", "Imposta", "Totale",
#                                          "Importo dovuto", "Stato e-fattura", "Stato"])
#         self.tabella["Data fattura"] = pd.to_datetime(self.tabella["Data fattura"])
    
#     def plot_andamenti(self, frequency, title):
#         grouped = self.tabella.groupby(self.tabella['Data fattura'].dt.year)
#         plt.figure(figsize=(12, 6))

#         for name, group in grouped:
#             # Creiamo una nuova colonna "Mese" per estrarre solo il mese dalla data della fattura
#             group['Mese'] = group['Data fattura'].dt.month
#             series = group.groupby('Mese')['Totale'].sum()

#             # Grafichiamo i dati
#             plt.plot(series.index, series, label=f'Dati {name}')

#         # Impostiamo le etichette dell'asse x come i nomi dei mesi
#         month_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#         plt.xticks(list(range(1, 13)), month_names, rotation=45)

#         plt.xlabel('Mese')
#         plt.ylabel('Totale')
#         plt.title(title)
#         plt.legend()
#         plt.grid(True)
        
#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         andamenti_img = Image.open(output)
#         return f"Andamento storico {frequency}:", andamenti_img
#     def plot_andamenti_trimestrali_per_annualita(self):
#         grouped = self.tabella.groupby(self.tabella['Data fattura'].dt.year)
#         plt.figure(figsize=(12, 6))

#         for name, group in grouped:
            
#             group['Trimestre'] = group['Data fattura'].dt.quarter
#             series = group.groupby('Trimestre')['Totale'].sum()

#             plt.plot(series.index, series, label=f'Dati {name}')

#         trimestre_names = ['Q1', 'Q2', 'Q3', 'Q4']
#         plt.xticks(list(range(1, 5)), trimestre_names, rotation=45)

#         plt.xlabel('Trimestre')
#         plt.ylabel('Totale')
#         plt.title('Andamenti Trimestrali per Annualità')
#         plt.legend()
#         plt.grid(True)
        
#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         andamenti_img = Image.open(output)# 
#         return "Andamento storico trimestrale per annualità:", andamenti_img


#     def plot_andamenti_mensili(self):
#         return self.plot_andamenti('M', 'Andamenti mensili')

#     def plot_andamenti_trimestrali(self):
#         return self.plot_andamenti_trimestrali_per_annualita()
    
# class Forecast:

#     def __init__(self, file_path):
#         self.tabella = pd.read_csv(file_path, header=None,
#                                    names=["Cliente", "Data fattura", "Numero", "Addetto vendite", "Data scadenza",
#                                          "Documento origine", "Insoluta", "Imponibile", "Imposta", "Totale",
#                                          "Importo dovuto", "Stato e-fattura", "Stato"])
#         self.tabella["Data fattura"] = pd.to_datetime(self.tabella["Data fattura"])

#     def get_min_value(self):
#         return self.tabella["Totale"].min()

#     def plot_forecast(self, frequency, title, steps):
#         series = self.tabella.set_index("Data fattura")["Totale"].resample(frequency).sum()

#         train_data = series[:'2023']
#         test_data = series['2024':'2026']

#         model = SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
#         model_fit = model.fit()

#         forecast = model_fit.get_forecast(steps=steps)
#         forecast_values = forecast.predicted_mean
#         conf_int = forecast.conf_int()
#         forecast_data = pd.DataFrame({
#             'Data': forecast_values.index,
#             'Previsione': forecast_values.values,
#             'Intervallo di confidenza (inferiore)': conf_int.iloc[:, 0].values,
#             'Intervallo di confidenza (superiore)': conf_int.iloc[:, 1].values
#         })

#         plt.plot(train_data.index, train_data, label='Dati storici')
#         plt.plot(test_data.index, test_data, label='Dati di test')
#         plt.plot(forecast_data['Data'], forecast_data['Previsione'], label='Previsioni')
#         plt.fill_between(forecast_data['Data'], forecast_data['Intervallo di confidenza (inferiore)'],
#                          forecast_data['Intervallo di confidenza (superiore)'], alpha=0.2, color='gray',
#                          label='Intervallo di confidenza')
#         plt.xlabel('Data')
#         plt.ylabel('Totale')
#         plt.title(title)
#         plt.legend()
#         plt.xticks(rotation=45)

#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         forecast_img = Image.open(output)

#         return f"Ecco l'andamento {frequency}:", forecast_img

#     def plot_previsioni_mensili(self):
#         return self.plot_forecast('M', 'Previsioni mensili', 36)

#     def plot_previsioni_trimestrali(self):
#         return self.plot_forecast('Q', 'Previsioni trimestrali', 14)

# class ChatHistory(models.Model):
#     _name = 'chat.history'
#     channel_id = fields.Many2one('mail.channel', required=True, ondelete='cascade')
#     role = fields.Selection([('user', 'User'), ('assistant', 'Assistant')], required=True)
#     content = fields.Text(required=True)
#     image_data = fields.Binary('Image') 
#     image_filename = fields.Char()
#     metadata = fields.Serialized()
#     image_metadata = fields.Serialized()
#     chart_type = fields.Selection([('trimestrial', 'Trimestrial'), ('monthly', 'Monthly')], string="Chart Type")
    
#     @api.model
#     def approximate_token_count(self, text):
#         return len(text.split())

#     @api.model
#     def _notify_thread(self, message, msg_vals=False, **kwargs):
#         rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
#         chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
#         user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
#         partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
#         author_id = msg_vals.get('author_id')
#         chatgpt_name = str(partner_chatgpt.name or '') + ', '
#         prompt = msg_vals.get('body')
        
#         if not prompt:
#             return rdata
#         openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
#         Partner = self.env['res.partner']
#         partner_name = ''
#         if author_id:
#             partner_id = Partner.browse(author_id)
#             if partner_id:
#                 partner_name = partner_id.name
#         if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         return rdata


# class Channel(models.Model):
#     _inherit = 'mail.channel'

#     @api.model
#     def approximate_token_count(self, text):
#         return len(text.split())

#     @api.model
#     def _notify_thread(self, message, msg_vals=False, **kwargs):
#         rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
#         chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
#         user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
#         partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
#         author_id = msg_vals.get('author_id')
#         chatgpt_name = str(partner_chatgpt.name or '') + ', '
#         prompt = msg_vals.get('body')
        
#         if not prompt:
#             return rdata
#         openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
#         Partner = self.env['res.partner']
#         partner_name = ''
#         if author_id:
#             partner_id = Partner.browse(author_id)
#             if partner_id:
#                 partner_name = partner_id.name
#         if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         return rdata
#     #nuovo tentativo di logica per separare in modo più netto le query legate agli andamenti trimestrali da quelle legate agli andamenti mensili
#     def _get_chatgpt_response(self, prompt, chat_history=[]):
        
#         andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
#         # previsioni_obj = Forecast(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
        
#         # Funzioni helper per separare la logica
#         def handle_trimestrial(prompt):
#             if "andamento trimestrale" in prompt.lower():
#                 reply, image = andamenti_obj.plot_andamenti_trimestrali()
#                 grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
#                 fatturato_per_annualita = {}
#                 max_fatturato_value, min_fatturato_value = float('-inf'), float('inf')
#                 max_fatturato_year, min_fatturato_year, max_fatturato_trimester, min_fatturato_trimester = None, None, None, None
                
#                 for name, group in grouped:
#                     group['Trimestre'] = group['Data fattura'].dt.quarter
#                     series = group.groupby('Trimestre')['Totale'].sum()
#                     if series.max() > max_fatturato_value:
#                         max_fatturato_value = series.max()
#                         max_fatturato_year = name
#                         max_fatturato_trimester = series.idxmax()

#                     if series.min() < min_fatturato_value:
#                         min_fatturato_value = series.min()
#                         min_fatturato_year = name
#                         min_fatturato_trimester = series.idxmin()

#                     fatturato_per_annualita[name] = {
#                         "fatturato_totale": series.sum(),
#                         "fatturato_max": series.max(),
#                         "fatturato_min": series.min()
#                     }

#                 metadata = {
#                     "fatturato_per_annualita": fatturato_per_annualita,
#                     "max_fatturato": {
#                         "year": int(max_fatturato_year),
#                         "trimester": int(max_fatturato_trimester),
#                         "value": float(max_fatturato_value)
#                     },
#                     "min_fatturato": {
#                         "year": int(min_fatturato_year),
#                         "trimester": int(min_fatturato_trimester),
#                         "value": float(min_fatturato_value)
#                     }
#                 }

#                 output = io.BytesIO()
#                 image.save(output, format='PNG')
#                 self.env['chat.history'].create({
#                     'channel_id': self.id,
#                     'role': 'assistant',
#                     'content': 'Vedi immagine allegata',
#                     'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
#                     'image_metadata': metadata,
#                     'chart_type': 'trimestrial'
#                 })

#                 trimestral_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Trimestrial Chart'>"
#                 return trimestral_html
            
#             last_image_metadata_trimestral = self.env['chat.history'].search(
#                 [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'trimestrial')],
#                 order='id desc', limit=1).image_metadata
            
#             if "fatturato totale" in prompt.lower():
#                 return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata_trimestral['fatturato_per_annualita']}"

#             if  "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
#                 max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
#                 fatturato_max_global = max(max_values)
#                 year = last_image_metadata_trimestral['max_fatturato']['year']
#                 trimester = last_image_metadata_trimestral['max_fatturato']['trimester']
#                 return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

#             if "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
#                 min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
#                 fatturato_min_global = min(min_values)
#                 year = last_image_metadata_trimestral['min_fatturato']['year']
#                 trimester = last_image_metadata_trimestral['min_fatturato']['trimester']
#                 return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

#             return None


#         def handle_monthly(prompt):
#             if "andamento mensile" in prompt.lower():
#                 reply, image = andamenti_obj.plot_andamenti_mensili()
#                 grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
#                 fatturato_per_annualita = {}
#                 max_fatturato_value, min_fatturato_value = float('-inf'), float('inf')
#                 max_fatturato_year, min_fatturato_year, max_fatturato_month, min_fatturato_month = None, None, None, None
                
#                 for name, group in grouped:
#                     group = group.copy()
#                     group['Mese'] = group['Data fattura'].dt.month
#                     series = group.groupby('Mese')['Totale'].sum()
#                     if series.max() > max_fatturato_value:
#                         max_fatturato_value = series.max()
#                         max_fatturato_year = name
#                         max_fatturato_month = series.idxmax()

#                     if series.min() < min_fatturato_value:
#                         min_fatturato_value = series.min()
#                         min_fatturato_year = name
#                         min_fatturato_month = series.idxmin()

#                     fatturato_per_annualita[name] = {
#                         "fatturato_totale": series.sum(),
#                         "fatturato_max": series.max(),
#                         "fatturato_min": series.min()
#                     }

#                 metadata = {
#                     "fatturato_per_annualita": fatturato_per_annualita,
#                     "max_fatturato": {
#                         "year": int(max_fatturato_year),
#                         "month": int(max_fatturato_month),
#                         "value": float(max_fatturato_value)
#                     },
#                     "min_fatturato": {
#                         "year": int(min_fatturato_year),
#                         "month": int(min_fatturato_month),
#                         "value": float(min_fatturato_value)
#                     }
#                 }

#                 output = io.BytesIO()
#                 image.save(output, format='PNG')
#                 self.env['chat.history'].create({
#                     'channel_id': self.id,
#                     'role': 'assistant',
#                     'content': 'Vedi immagine allegata',
#                     'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
#                     'image_metadata': metadata,
#                     'chart_type': 'monthly'
#                 })

#                 monthly_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Monthly Chart'>"
#                 return monthly_html
            
#             last_image_metadata_monthly = self.env['chat.history'].search(
#                 [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'monthly')],
#                 order='id desc', limit=1).image_metadata
            
#             if last_image_metadata_monthly and "fatturato totale" in prompt.lower():
#                 return f"I fatturati totali per ciascun anno e con relativi picchi mensili sono stati i seguenti: {last_image_metadata_monthly['fatturato_per_annualita']}"

#             if last_image_metadata_monthly and ("massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower()):
#                 max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_monthly['fatturato_per_annualita'].values()]
#                 fatturato_max_global = max(max_values)
#                 year = last_image_metadata_monthly['max_fatturato']['year']
#                 month = last_image_metadata_monthly['max_fatturato']['month']
#                 return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {month}° mese dell'anno {year}."

#             if last_image_metadata_monthly and ("minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower()):
#                 min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_monthly['fatturato_per_annualita'].values()]
#                 fatturato_min_global = min(min_values)
#                 year = last_image_metadata_monthly['min_fatturato']['year']
#                 month = last_image_metadata_monthly['min_fatturato']['month']
#                 return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {month}° mese dell'anno {year}."

#             return None
#         # Chiamate principali
#         response = handle_trimestrial(prompt)
#         if response:
#             return response
        
#         response = handle_monthly(prompt)
#         if response:
#             return response

#         # return "Non ho potuto elaborare la tua richiesta."
#         else:
#             ICP = self.env['ir.config_parameter'].sudo()
#             openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
#             gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
#             gpt_model = 'gpt-3.5-turbo'
#             try:
#                 if gpt_model_id:
#                     gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
#             except Exception as ex:
#                 gpt_model = 'gpt-3.5-turbo'
#                 pass
            
#             user_message = {"role": "user", "content": prompt}
            
#             chat_history.append(user_message)
            
#             total_tokens = sum(len(msg["content"].split()) for msg in chat_history)  # this is a naive token estimate by counting words
            
#             # safety_margin = 500
            
#             max_response_tokens = 1500 - total_tokens
            
#             while max_response_tokens <= 0:
#                 removed_message = chat_history.pop(0)  # remove the oldest message
#                 total_tokens -= len(removed_message["content"].split())  # update total_tokens
#                 max_response_tokens = 1500 - total_tokens
#             try:
#                 chat = openai.ChatCompletion.create(
#                 model=gpt_model,
#                 messages=chat_history,
#                 temperature=0.6,
#                 max_tokens=max_response_tokens,  # the remaining tokens available
#             )
#                 assistant_reply = chat.choices[0].message['content']
                
#                 chat_history.append({"role": "assistant", "content": assistant_reply})
                
#                 return assistant_reply
#             except Exception as e:
#                 print("An error occurred:", e)
#                 raise UserError(_("An error occurred: %s") % e)
            
# FINE CODICE FONDAMENTALE


    #         Funzione da ottimizzare per separare in modo più netto le query legate agli andamenti mensili da quelle legate agli andamenti trimestrali
    # def _get_chatgpt_response(self, prompt, chat_history=[]):
    #     andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
    #     previsioni_obj = Forecast(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")

    #     if "andamento trimestrale" in prompt.lower():
    #         reply, image = andamenti_obj.plot_andamenti_trimestrali()
    #         grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #         fatturato_per_annualita = {}
    #         #RETTIFICHE#INIZIO
    #         max_fatturato_value = float('-inf')
    #         max_fatturato_year = None
    #         max_fatturato_trimester = None

    #         min_fatturato_value = float('inf')
    #         min_fatturato_year = None
    #         min_fatturato_trimester = None
    #         #FINE
    #         for name, group in grouped:
    #             group['Trimestre'] = group['Data fattura'].dt.quarter
    #             series = group.groupby('Trimestre')['Totale'].sum()
    #             #RETTIFICHE#INIZIO
    #             if series.max() > max_fatturato_value:
    #                 max_fatturato_value = series.max()
    #                 max_fatturato_year = name
    #                 max_fatturato_trimester = series.idxmax()

    #             if series.min() < min_fatturato_value:
    #                 min_fatturato_value = series.min()
    #                 min_fatturato_year = name
    #                 min_fatturato_trimester = series.idxmin()
    #                 #FINE

    #             fatturato_per_annualita[name] = {
    #                 "fatturato_totale": series.sum(),
    #                 "fatturato_max": series.max(),
    #                 "fatturato_min": series.min()
    #             }
    #         metadata = {
    #             "fatturato_per_annualita": fatturato_per_annualita,
    #             #RETTIFICHE INIZIO
    #             "max_fatturato": {
    #             "year": int(max_fatturato_year),
    #             "trimester": int(max_fatturato_trimester),
    #             "value": float(max_fatturato_value)
    #         },
    #             "min_fatturato": {
    #                 "year": int(min_fatturato_year),
    #                 "trimester": int(min_fatturato_trimester),
    #                 "value": float(min_fatturato_value)
    #             }


    #         }

    #         # Memorizza l'immagine e i metadati nella chat history
    #         output = io.BytesIO()
    #         image.save(output, format='PNG')
    #         self.env['chat.history'].create({
    #                 'channel_id': self.id,
    #                 'role': 'assistant',
    #                 'content': 'Vedi immagine allegata',
    #                 'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #                 'image_metadata': metadata,
    #                 'chart_type': 'trimestrial'
    #             })

    #         trimestral_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Trimestrial Chart'>"
    #         return trimestral_html
    #     last_image_metadata_trimestral = self.env['chat.history'].search(
    #         [('channel_id', '=', self.id), ('content', '=', "Ecco a te l'andamento trimestrale richiesto"),('image_data', '!=', False), ('chart_type', '=', 'trimestrial')],
    #         order='id desc', limit=1).image_metadata
    #     # last_image_metadata_trimestral = self.env['chat.history'].search([('channel_id', '=', self.id), ('image_data', '!=', False)], order='id desc', limit=1).image_metadata
    #     if last_image_metadata_trimestral and "fatturato totale" in prompt.lower():
    #         fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata_trimestral['fatturato_per_annualita'].items()}  
    #         return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata_trimestral['fatturato_per_annualita']}"
    #     if last_image_metadata_trimestral and "massimo fatturato" and "fatturato massimo" in prompt.lower():
    #         max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
    #         fatturato_max_global = max(max_values)
    #         year = last_image_metadata_trimestral['max_fatturato']['year']
    #         trimester = last_image_metadata_trimestral['max_fatturato']['trimester']
    #         return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

    #     if last_image_metadata_trimestral and "minimo fatturato" and "fatturato minimo" in prompt.lower():
    #         min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
    #         fatturato_min_global = min(min_values)
    #         year = last_image_metadata_trimestral['min_fatturato']['year']
    #         trimester = last_image_metadata_trimestral['min_fatturato']['trimester']
    #         return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."
        

    #     elif "andamento mensile" in prompt.lower():
    #         reply, image = andamenti_obj.plot_andamenti_mensili()
    #         grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #         fatturato_per_annualita = {}
            
    #         max_fatturato_value = float('-inf')
    #         max_fatturato_year = None
    #         max_fatturato_month = None

    #         min_fatturato_value = float('inf')
    #         min_fatturato_year = None
    #         min_fatturato_month = None
            
    #         for name, group in grouped:
    #             group = group.copy()
    #             group['Mese'] = group['Data fattura'].dt.month
    #             series = group.groupby('Mese')['Totale'].sum()
                
    #             if series.max() > max_fatturato_value:
    #                 max_fatturato_value = series.max()
    #                 max_fatturato_year = name
    #                 max_fatturato_month = series.idxmax()

    #             if series.min() < min_fatturato_value:
    #                 min_fatturato_value = series.min()
    #                 min_fatturato_year = name
    #                 min_fatturato_month = series.idxmin()

    #             fatturato_per_annualita[name] = {
    #                 "fatturato_totale": series.sum(),
    #                 "fatturato_max": series.max(),
    #                 "fatturato_min": series.min()
    #             }

    #         metadata = {
    #             "fatturato_per_annualita": fatturato_per_annualita,
    #             "max_fatturato": {
    #                 "year": int(max_fatturato_year),
    #                 "month": int(max_fatturato_month),
    #                 "value": float(max_fatturato_value)
    #             },
    #             "min_fatturato": {
    #                 "year": int(min_fatturato_year),
    #                 "month": int(min_fatturato_month),
    #                 "value": float(min_fatturato_value)
    #             }
    #         }

    #         # Memorizza l'immagine e i metadati nella chat history
    #         output = io.BytesIO()
    #         image.save(output, format='PNG')
    #         self.env['chat.history'].create({
    #                 'channel_id': self.id,
    #                 'role': 'assistant',
    #                 'content': 'Vedi immagine allegata',
    #                 'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #                 'image_metadata': metadata,
    #                 'chart_type': 'monthly'
    #             })

    #         mensile_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Monthly Chart'>"
    #         return mensile_html
        
    #     # last_image_metadata_mensile = self.env['chat.history'].search([('channel_id', '=', self.id), ('image_data', '!=', False)], order='id desc', limit=1).image_metadata
    #     last_image_metadata_mensile = self.env['chat.history'].search(
    #         [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'monthly')],
    #         order='id desc', limit=1).image_metadata
    #     if last_image_metadata_mensile and "fatturato totale" in prompt.lower():
    #         fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata_mensile['fatturato_per_annualita'].items()}  
    #         return f"I fatturati totali per ciascun anno e con relativi picchi mensili sono stati i seguenti: {last_image_metadata_mensile['fatturato_per_annualita']}"
   

    #     if last_image_metadata_mensile and (("massimo fatturato" in prompt.lower()) or ("fatturato massimo" in prompt.lower())):
    #         max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_mensile['fatturato_per_annualita'].values()]
    #         fatturato_max_global = max(max_values)
    #         year = last_image_metadata_mensile['max_fatturato']['year']
    #         month = last_image_metadata_mensile['max_fatturato']['month']
    #         return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {month}° mese dell'anno {year}."

    #     if last_image_metadata_mensile and (("minimo fatturato" in prompt.lower()) or ("fatturato minimo" in prompt.lower())):
    #         min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_mensile['fatturato_per_annualita'].values()]
    #         fatturato_min_global = min(min_values)
    #         year = last_image_metadata_mensile['min_fatturato']['year']
    #         month = last_image_metadata_mensile['min_fatturato']['month']
    #         return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {month}° mese dell'anno {year}."

   
        
        
    #     elif "previsioni mensili" in prompt.lower():
    #         reply, image= previsioni_obj.plot_previsioni_mensili()
    #         output= io.BytesIO()
    #         image.save(output, format='PNG')
    #         b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

    #         img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Monthly Forecast'>"

    #         return img_html
    #     elif "previsioni trimestrali" in prompt.lower():
    #         reply, image= previsioni_obj.plot_previsioni_trimestrali()
    #         output= io.BytesIO()
    #         image.save(output, format='PNG')
    #         b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

    #         img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Trimestral Forecast'>"

    #         return img_html
    
    
    #     ICP = self.env['ir.config_parameter'].sudo()
    #     openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
    #     gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
    #     gpt_model = 'gpt-3.5-turbo'
    #     try:
    #         if gpt_model_id:
    #             gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
    #     except Exception as ex:
    #         gpt_model = 'gpt-3.5-turbo'
    #         pass
        
    #     user_message = {"role": "user", "content": prompt}
        
    #     chat_history.append(user_message)
        
    #     total_tokens = sum(len(msg["content"].split()) for msg in chat_history)  # this is a naive token estimate by counting words
        
    #     # safety_margin = 500
        
    #     max_response_tokens = 1500 - total_tokens
        
    #     while max_response_tokens <= 0:
    #         removed_message = chat_history.pop(0)  # remove the oldest message
    #         total_tokens -= len(removed_message["content"].split())  # update total_tokens
    #         max_response_tokens = 1500 - total_tokens
    #     try:
    #         chat = openai.ChatCompletion.create(
    #         model=gpt_model,
    #         messages=chat_history,
    #         temperature=0.6,
    #         max_tokens=max_response_tokens,  # the remaining tokens available
    #     )
    #         assistant_reply = chat.choices[0].message['content']
            
    #         chat_history.append({"role": "assistant", "content": assistant_reply})
            
    #         return assistant_reply
    #     except Exception as e:
    #         print("An error occurred:", e)
    #         raise UserError(_("An error occurred: %s") % e)



# io vorrei, oltre a poter fare domande di default legate all'uso di chatgpt 3.5 turbo, anche fare alcune domande flessibili sulle fatture al chatbot del tipo:
# 1) Potrei avere il bilancio mensile di gennaio 2023?
# 2) Qual è stato l'andamento trimestrale nel 2022
#QUESTO CODICE VA, MI FA ACCEDERE AL SERVER

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import io
from PIL import Image
from statsmodels.tsa.statespace.sarimax import SARIMAX
import openai
import base64
import odoo
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import datetime
from textwrap import wrap



class Andamenti:
    def __init__(self, file_path):
        self.tabella = pd.read_csv(file_path, header=None,
                                   names=["Cliente", "Data fattura", "Numero", "Addetto vendite", "Data scadenza",
                                         "Documento origine", "Insoluta", "Imponibile", "Imposta", "Totale",
                                         "Importo dovuto", "Stato e-fattura", "Stato"])
        self._prepare_data()
    def indice_affidabilità(self, tipo="affidabile", soglia_fatture=10, coefficiente_calibrazione=0.5):
        counting_clienti = self.tabella["Cliente"].nunique()
        stato_fatture_cliente = self.tabella.groupby("Cliente")["Stato e-fattura"].value_counts().unstack(fill_value=0)

        totale_fatture_cliente = stato_fatture_cliente.sum(axis=1)
        fatture_pagate_cliente = stato_fatture_cliente.get(" Pagata", pd.Series([0]*len(stato_fatture_cliente.index), index=stato_fatture_cliente.index))
        solvibilità_cliente = (fatture_pagate_cliente / totale_fatture_cliente) * 100

        # Calibrare l'affidabilità
        mask = totale_fatture_cliente < soglia_fatture
        solvibilità_cliente[mask] = solvibilità_cliente[mask] * coefficiente_calibrazione
        
        # Selezionare i clienti in base al tipo
        if tipo == "affidabile":
            clienti_selezionati = solvibilità_cliente.sort_values(ascending=False).head(10)
            color = "green"
            title = "10 clienti più affidabili"
        else:  # tipo == "meno"
            clienti_selezionati = solvibilità_cliente.sort_values().head(10)
            color = "red"
            title = "10 clienti meno affidabili"
        
        # Creazione del grafico
        plt.figure(figsize=(12, 10))
        clienti_selezionati.plot(kind="bar", color=color, label=title)
        plt.title(title)
        plt.xlabel("Cliente")
        plt.ylabel("Ratio (%)")
        fatture_labels = ['\n'.join(wrap(label, 15)) for label in clienti_selezionati.index]
        plt.xticks(range(len(fatture_labels)), fatture_labels, rotation=45, ha='right', fontsize=10)

        # Converti il grafico in un'immagine
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='PNG')
        image_buffer.seek(0)  # Reset del buffer alla posizione iniziale
        reliability_chart = f"<img src='data:image/png;base64,{base64.b64encode(image_buffer.getvalue()).decode('utf-8')}' alt='{title}'>"
        
        return f"Ecco l'indice di affidabilità dei {title}", reliability_chart




    # def indice_affidabilità(self):
    #     counting_clienti = self.tabella["Cliente"].nunique()
    #     stato_fatture_cliente = self.tabella.groupby("Cliente")["Stato e-fattura"].value_counts().unstack(fill_value=0)

    #     totale_fatture_cliente = stato_fatture_cliente.sum(axis=1).sort_values(ascending=False).head(counting_clienti)
    #     fatture_pagate_cliente = stato_fatture_cliente[" Pagata"]
    #     solvibilità_cliente = (fatture_pagate_cliente / totale_fatture_cliente) * 100

    #     plt.figure(figsize=(12, 10))
    #     solvibilità_cliente.plot(kind="bar", color="red")
    #     plt.title("Fatture Pagate/Fatture totali per cliente")
    #     plt.xlabel("Cliente")
    #     plt.ylabel("Ratio (%)")
    #     fatture_labels = ['\n'.join(wrap(label, 15)) for label in solvibilità_cliente.index]
    #     plt.xticks(range(len(fatture_labels)), fatture_labels, rotation=45, ha='right', fontsize=10)
        
    #     # Converti il grafico in un'immagine
    #     image_buffer = io.BytesIO()
    #     plt.savefig(image_buffer, format='PNG')
    #     image_buffer.seek(0)  # Reset del buffer alla posizione iniziale
    #     reliability_chart = f"<img src='data:image/png;base64,{base64.b64encode(image_buffer.getvalue()).decode('utf-8')}' alt='Reliability Chart'>"
        
    #     return "Ecco l'indice di affidabilità dei clienti di Unitiva", reliability_chart
        
    def informazioni_affidabilità_cliente(self, nome_cliente):
        cliente_data = self.tabella[self.tabella["Cliente"] == nome_cliente]
        if not cliente_data.empty:
            totale_fatture_cliente = cliente_data["Stato e-fattura"].count()
            fatture_pagate_cliente = cliente_data[cliente_data["Stato e-fattura"] == "Pagata"]["Stato e-fattura"].count()
            solvibilità_cliente = (fatture_pagate_cliente / totale_fatture_cliente) * 100

            return f"Informazioni sull'affidabilità di {nome_cliente}:\n" \
                   f"Percentuale fatture pagate: {solvibilità_cliente:.2f}%"
        else:
            return f"Il cliente {nome_cliente} non è presente nei dati."
    
    
    #Questa linea di codice mi genera gli andamenti mensili relativi alle varie annualità in simultanea, sullo stesso grafico
    # def plot_andamenti(self, frequency, title):


        # plt.figure(figsize=(12, 6))

        # for name, group in grouped:
        #     # Creiamo una nuova colonna "Mese" per estrarre solo il mese dalla data della fattura
        #     group['Mese'] = group['Data fattura'].dt.month
        #     series = group.groupby('Mese')['Totale'].sum()

        #     # Grafichiamo i dati
        #     plt.plot(series.index, series, label=f'Dati {name}')

        # La restante parte della funzione dovrebbe essere la stessa

    def plot_andamenti_mensili(self, year):
    
        year_data = self.tabella[self.tabella['Anno'] == year]
        
        year_data['Mese'] = year_data['Data fattura'].dt.month
        series = year_data.groupby('Mese')['Totale'].sum()
        
        plt.figure(figsize=(12, 6))
        plt.plot(series.index, series, label=f'Dati {year}')

        month_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        plt.xticks(list(range(1, 13)), month_names, rotation=45)

        plt.xlabel('Mese')
        plt.ylabel('Totale')
        plt.title(f'Andamenti Mensili {year}')
        plt.legend()
        plt.grid(True)
        
        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        andamenti_img = Image.open(output)
        return f"Andamento storico {year}:", andamenti_img
        
                       
    
    def plot_andamenti_trimestrali_per_anno(self, year):
        year_data = self.tabella[self.tabella['Anno'] == year]
        
        year_data['Trimestre'] = year_data['Data fattura'].dt.quarter
        series = year_data.groupby('Trimestre')['Totale'].sum()
        
        plt.figure(figsize=(12, 6))
        plt.plot(series.index, series, label=f'Dati {year}')
        
        trimestre_names = ['Q1', 'Q2', 'Q3', 'Q4']
        plt.xticks(list(range(1, 5)), trimestre_names, rotation=45)
        plt.xlabel('Trimestre')
        plt.ylabel('Totale')
        plt.title(f'Andamenti Trimestrali {year}')
        plt.legend()
        plt.grid(True)
        
        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        andamenti_img = Image.open(output)
        
        return f"Andamento trimestrale {year}:", andamenti_img



    # def plot_andamenti_mensili(self):
    #     return self.plot_andamenti(year)


    def _prepare_data(self):
        # Converti la colonna 'Data' in datetime
        self.tabella['Data fattura'] = pd.to_datetime(self.tabella['Data fattura'])

        # Estrai il mese e l'anno e crea nuove colonne
        self.tabella['Mese'] = self.tabella['Data fattura'].dt.month
        self.tabella['Anno'] = self.tabella['Data fattura'].dt.year

    def get_monthly_balance(self, month, year):
        # Filtro il DataFrame per il mese e l'anno specificati e calcolo il bilancio mensile
        monthly_data = self.tabella[(self.tabella['Mese'] == month) & (self.tabella['Anno'] == year)]
        return sum(monthly_data['Totale'])

    def get_trimestral_balance(self, month, year):
        # Calcolo il bilancio trimestrale in base al mese specificato
        if month in [1, 2, 3]:
            quarter = [1, 2, 3]
        elif month in [4, 5, 6]:
            quarter = [4, 5, 6]
        elif month in [7, 8, 9]:
            quarter = [7, 8, 9]
        else:
            quarter = [10, 11, 12]

        quarterly_data = self.tabella[(self.tabella['Mese'].isin(quarter)) & (self.tabella['Anno'] == year)]
        return sum(quarterly_data['Totale'])

def get_month_from_prompt(prompt):
    months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
    for index, month in enumerate(months, 1):
        if month in prompt.lower():
            return index
    return None

def get_year_from_prompt(prompt):

    for year in range(2000, datetime.now().year + 1):
        if str(year) in prompt:
            return year
    return None
class ChatHistory(models.Model):
    _name = 'chat.history'
    channel_id = fields.Many2one('mail.channel', required=True, ondelete='cascade')
    role = fields.Selection([('user', 'User'), ('assistant', 'Assistant')], required=True)
    content = fields.Text(required=True)
    image_data = fields.Binary('Image') 
    image_filename = fields.Char()
    metadata = fields.Serialized()
    image_metadata = fields.Serialized()
    chart_type = fields.Selection([('trimestrial', 'Trimestrial'), ('monthly', 'Monthly')], string="Chart Type")
    
    @api.model
    def approximate_token_count(self, text):
        return len(text.split())

    @api.model
    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
        user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
        partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        prompt = msg_vals.get('body')
        
        if not prompt:
            return rdata
        openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
        Partner = self.env['res.partner']
        partner_name = ''
        if author_id:
            partner_id = Partner.browse(author_id)
            if partner_id:
                partner_name = partner_id.name
        if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
            try:
                res = self._get_chatgpt_response(prompt=prompt)
                self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))

        elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
            try:
                res = self._get_chatgpt_response(prompt=prompt)
                chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))

        return rdata


class Channel(models.Model):
    _inherit = 'mail.channel'

    

    
        
    def estrai_nome_cliente_da_prompt(self, prompt):
        andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
        index = prompt.lower().find("cliente")
        if index == -1:
            return None  # Non ha trovato la parola "cliente" nel prompt
        
        # Estrae il nome del cliente dal prompt
        cliente_part = prompt[index + len("cliente"):].strip()
        
        # Verifica se il nome del cliente è nel dataset
        if cliente_part in andamenti_obj.data["Cliente"].values:
            return cliente_part
        else:
            return None


    @api.model
    def approximate_token_count(self, text):
        return len(text.split())

    @api.model
    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
        user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
        partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        prompt = msg_vals.get('body')
        
        if not prompt:
            return rdata
        openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
        Partner = self.env['res.partner']
        partner_name = ''
        if author_id:
            partner_id = Partner.browse(author_id)
            if partner_id:
                partner_name = partner_id.name
        if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
            try:
                res = self._get_chatgpt_response(prompt=prompt)
                self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))

        elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
            try:
                res = self._get_chatgpt_response(prompt=prompt)
                chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))

        return rdata
    

    @api.model
    def _get_chatgpt_response(self, prompt, chat_history=[]):
        andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")

        if "affidabilità" in prompt.lower():
            if "migliori clienti" in prompt.lower():
                title, image = andamenti_obj.indice_affidabilità(tipo="affidabile")
                return title, image
            elif "peggiori clienti" in prompt.lower():
                title, image = andamenti_obj.indice_affidabilità(tipo="meno")
                return title, image
            elif "cliente" in prompt.lower():
                nome_cliente = self.estrai_nome_cliente_da_prompt(prompt)
                print(nome_cliente)
                if nome_cliente:
                    return andamenti_obj.informazioni_affidabilità_cliente(nome_cliente)
                else:
                    return "Non ho capito il nome del cliente."
            else:
                return "Non ho capito la tua richiesta sull'affidabilità."


        def handle_trimestrial_graphic(prompt):
            year = None
            if "andamento trimestrale" in prompt.lower():
                year = get_year_from_prompt(prompt)
            if year:
                reply, image = andamenti_obj.plot_andamenti_trimestrali_per_anno(year)
                grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
                fatturato_per_annualita = {}
                max_fatturato_value, min_fatturato_value = float('-inf'), float('inf')
                max_fatturato_year, min_fatturato_year, max_fatturato_trimester, min_fatturato_trimester = None, None, None, None
                
                for name, group in grouped:
                    group['Trimestre'] = group['Data fattura'].dt.quarter
                    series = group.groupby('Trimestre')['Totale'].sum()
                    if series.max() > max_fatturato_value:
                        max_fatturato_value = series.max()
                        max_fatturato_year = name
                        max_fatturato_trimester = series.idxmax()

                    if series.min() < min_fatturato_value:
                        min_fatturato_value = series.min()
                        min_fatturato_year = name
                        min_fatturato_trimester = series.idxmin()

                    fatturato_per_annualita[name] = {
                        "fatturato_totale": series.sum(),
                        "fatturato_max": series.max(),
                        "fatturato_min": series.min()
                    }

                metadata = {
                    "fatturato_per_annualita": fatturato_per_annualita,
                    "max_fatturato": {
                        "year": int(max_fatturato_year),
                        "trimester": int(max_fatturato_trimester),
                        "value": float(max_fatturato_value)
                    },
                    "min_fatturato": {
                        "year": int(min_fatturato_year),
                        "trimester": int(min_fatturato_trimester),
                        "value": float(min_fatturato_value)
                    }
                }

                output = io.BytesIO()
                image.save(output, format='PNG')
                self.env['chat.history'].create({
                    'channel_id': self.id,
                    'role': 'assistant',
                    'content': 'Vedi immagine allegata',
                    'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
                    'image_metadata': metadata,
                    'chart_type': 'trimestrial'
                })

                trimestral_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Trimestrial Chart'>"
                return trimestral_html
            # year= None
            #Mantieni queste poche righe per il momento
            # if "andamento trimestrale nel" not in prompt.lower():
            #     return None
            # year = get_year_from_prompt(prompt)
            # if year:
            #     img = andamenti_obj.plot_andamenti_trimestrali_per_anno(year)
            #     return img
            # return None

            
            # last_image_metadata_trimestral = self.env['chat.history'].search(
            #     [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'trimestrial')],
            #     order='id desc', limit=1).image_metadata
            
            # if "fatturato totale" in prompt.lower():
            #     return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata_trimestral['fatturato_per_annualita']}"

            # if  "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
            #     max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
            #     fatturato_max_global = max(max_values)
            #     year = last_image_metadata_trimestral['max_fatturato']['year']
            #     trimester = last_image_metadata_trimestral['max_fatturato']['trimester']
            #     return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

            # if "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
            #     min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
            #     fatturato_min_global = min(min_values)
            #     year = last_image_metadata_trimestral['min_fatturato']['year']
            #     trimester = last_image_metadata_trimestral['min_fatturato']['trimester']
            #     return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

            # return None
        def handle_monthly_graphic(prompt):
            year= None
            if "andamento mensile" in prompt.lower():
                year= get_year_from_prompt(prompt)
            if year:
                reply, image = andamenti_obj.plot_andamenti_mensili(year)
                grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
                fatturato_per_annualita = {}
                max_fatturato_value, min_fatturato_value = float('-inf'), float('inf')
                max_fatturato_year, min_fatturato_year, max_fatturato_month, min_fatturato_month = None, None, None, None
                
                for name, group in grouped:
                    # group = group.copy()
                    group['Mese'] = group['Data fattura'].dt.month
                    series = group.groupby('Mese')['Totale'].sum()
                    if series.max() > max_fatturato_value:
                        max_fatturato_value = series.max()
                        max_fatturato_year = name
                        max_fatturato_month = series.idxmax()

                    if series.min() < min_fatturato_value:
                        min_fatturato_value = series.min()
                        min_fatturato_year = name
                        min_fatturato_month = series.idxmin()

                    fatturato_per_annualita[name] = {
                        "fatturato_totale": series.sum(),
                        "fatturato_max": series.max(),
                        "fatturato_min": series.min()
                    }

                metadata = {
                    "fatturato_per_annualita": fatturato_per_annualita,
                    "max_fatturato": {
                        "year": int(max_fatturato_year),
                        "month": int(max_fatturato_month),
                        "value": float(max_fatturato_value)
                    },
                    "min_fatturato": {
                        "year": int(min_fatturato_year),
                        "month": int(min_fatturato_month),
                        "value": float(min_fatturato_value)
                    }
                }

                output = io.BytesIO()
                image.save(output, format='PNG')
                self.env['chat.history'].create({
                    'channel_id': self.id,
                    'role': 'assistant',
                    'content': 'Vedi immagine allegata',
                    'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
                    'image_metadata': metadata,
                    'chart_type': 'monthly'
                })

                monthly_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Monthly Chart'>"
                return monthly_html
            
            # last_image_metadata_monthly = self.env['chat.history'].search(
            #     [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'monthly')],
            #     order='id desc', limit=1).image_metadata
            
            # if last_image_metadata_monthly and "fatturato totale" in prompt.lower():
            #     return f"I fatturati totali per ciascun anno e con relativi picchi mensili sono stati i seguenti: {last_image_metadata_monthly['fatturato_per_annualita']}"

            # if last_image_metadata_monthly and ("massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower()):
            #     max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_monthly['fatturato_per_annualita'].values()]
            #     fatturato_max_global = max(max_values)
            #     year = last_image_metadata_monthly['max_fatturato']['year']
            #     month = last_image_metadata_monthly['max_fatturato']['month']
            #     return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {month}° mese dell'anno {year}."

            # if last_image_metadata_monthly and ("minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower()):
            #     min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_monthly['fatturato_per_annualita'].values()]
            #     fatturato_min_global = min(min_values)
            #     year = last_image_metadata_monthly['min_fatturato']['year']
            #     month = last_image_metadata_monthly['min_fatturato']['month']
            #     return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {month}° mese dell'anno {year}."

            # return None

        def handle_trimestrial_info(prompt):
            if "trimestrale" not in prompt.lower():
                return None
            month = get_month_from_prompt(prompt)
            year = get_year_from_prompt(prompt)
            if month and year:
                res = andamenti_obj.get_trimestral_balance(month, year)
                if res:
                    return res
            return None

        def handle_monthly_info(prompt):
            if "mensile" not in prompt.lower():
                return None
            month = get_month_from_prompt(prompt)
            year = get_year_from_prompt(prompt)
            if month and year:
                res = andamenti_obj.get_monthly_balance(month, year)
                if res:
                    return res
            return None

        
    

        # def handle_trimestrial_graphic(prompt):
        #     if "andamento trimestrale nel" not in prompt.lower():
        #         return None
        #     year = get_year_from_prompt(prompt)
        #     if year:
        #         title, img = andamenti_obj.plot_andamenti_trimestrali_per_anno(year)
        #         return img
        #     return None
        # Chiamate principali
        #Estrazione cliente migliore o peggiore
        # result= estrai_nome_cliente_da_prompt(prompt)
        # if result:
        #     return result
        #Ottenimento grafici degli andamenti
        result= handle_monthly_graphic(prompt)
        if result: 
            return result 
        result = handle_trimestrial_graphic(prompt)
        if result: 
            return result 
        #Ottenimento infomrazioni sugli andamenti
        response = handle_trimestrial_info(prompt)
        if response:
            return response
        
        response = handle_monthly_info(prompt)
        if response:
            return response
        
        # response = handle_trimestrial_graphic(prompt)
        # if response:
        #     return response
        
        # response = handle_monthly_graphic(prompt)
        if response:
            return response
        if "trimestrale" in prompt.lower() and "andamento trimestrale nel" not in prompt.lower():
            response = handle_trimestrial_graphic(prompt)
        elif "mensile" in prompt.lower():
            response = handle_monthly_graphic(prompt)
        elif "andamento trimestrale nel" in prompt.lower():
            response = handle_trimestrial_graphic(prompt)

        if response:
            return response
        # return "Mi dispiace, non sono stato in grado di elaborare la tua richiesta."

        # return "Non ho potuto elaborare la tua richiesta."
        
    
        ICP = self.env['ir.config_parameter'].sudo()
        openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
        gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
        gpt_model = 'gpt-3.5-turbo'
        # gpt_model = 'gpt-4'
        try:
            if gpt_model_id:
                gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
        except Exception as ex:
            gpt_model = 'gpt-3.5-turbo'
            # gpt_model = 'gpt-4'
            pass
        
        user_message = {"role": "user", "content": prompt}
        
        chat_history.append(user_message)
        
        total_tokens = sum(len(msg["content"].split()) for msg in chat_history)  # this is a naive token estimate by counting words
        
        # safety_margin = 500
        
        max_response_tokens = 1500 - total_tokens
        
        while max_response_tokens <= 0:
            removed_message = chat_history.pop(0)  # remove the oldest message
            total_tokens -= len(removed_message["content"].split())  # update total_tokens
            max_response_tokens = 1500 - total_tokens
        try:
            chat = openai.ChatCompletion.create(
            model=gpt_model,
            messages=chat_history,
            temperature=0.6,
            max_tokens=max_response_tokens,  # the remaining tokens available
        )
            assistant_reply = chat.choices[0].message['content']
            
            chat_history.append({"role": "assistant", "content": assistant_reply})
            
            return assistant_reply
        except Exception as e:
            print("An error occurred:", e)
            raise UserError(_("An error occurred: %s") % e)

        # response = None
        # if "trimestrale" in prompt.lower() and "andamento trimestrale nel" not in prompt.lower():
        #     response = handle_trimestrial(prompt)
        # elif "mensile" in prompt.lower():
        #     response = handle_monthly(prompt)
        # elif "andamento trimestrale nel" in prompt.lower():
        #     response = handle_trimestrial_graphic(prompt)

        # if response:
        #     return response
        # return "Mi dispiace, non sono stato in grado di elaborare la tua richiesta."

# Ensure you're connected to the database and have a cursor (cr) and a user id (uid) available
# ... (import statements and other code)

# Create a new chat channel
# new_channel = self.env['mail.channel'].create({
#     'name': 'ChatGPT Channel',  # Replace with the desired channel name
#     'public': 'private',  # Set to 'public' if you want a public channel
# })

# # Add a message to the channel
# new_channel.message_post(body="Hello, this is a test message!")

# # Retrieve the chatbot channel
# chatbot_channel = self.env['mail.channel'].search([('name', '=', 'ChatGPT Channel')])

# # Check if the chatbot channel exists and use your methods
# if chatbot_channel:
#     andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")

#     prompts = [
#         "Bilancio mensile di febbraio 2023",
#         "Bilancio mensile di giugno 2023",
#     ]
    
#     for prompt in prompts:
#         response = chatbot_channel._get_chatgpt_response(prompt)
#         print(f"Prompt: {prompt}")
#         if isinstance(response, Image.Image):
#             response.show()
#         else:
#             print(f"Il bilancio mensile è stato di: {response}")

#     response = chatbot_channel._get_chatgpt_response("Qual è stato l'andamento trimestrale nel 2023")
#     if isinstance(response, Image.Image):
#         response.show()
#     else:
#         print(response)
        
#     response_2023 = chatbot_channel._get_chatgpt_response("Potrei avere il bilancio mensile di gennaio 2023")
#     print(f"Il bilancio è stato pari a:", response_2023)

#     response = chatbot_channel._get_chatgpt_response("Qual è stato l'andamento trimestrale nel 2022")
#     if isinstance(response, Image.Image):
#         response.show()
#     else:
#         print(response)


    def your_method_inside_some_model(self):
        chatbot = self.env['mail.channel'].search([], limit=1)

        if chatbot:
            prompts = ["Bilancio mensile di febbraio 2023", "Bilancio mensile di giugno 2023"]
            for prompt in prompts:
                response = chatbot._get_chatgpt_response(prompt)
                print(f"Prompt: {prompt}")
                if isinstance(response, Image.Image):
                    response.show()
                else:
                    print(f"Il bilancio mensile è stato di : {response}")

            response = chatbot._get_chatgpt_response("Qual è stato l'andamento trimestrale nel 2023")
            if isinstance(response, Image.Image):
                response.show()
            else:
                print(response)



        

            

# #Esempio di utilizzo#oppure
# chatbot = Channel()
# response_2023 = chatbot._get_chatgpt_response("Potrei avere il bilancio mensile di gennaio 2023")
# print(f"Il bilancio è stato pari a:", response_2023)


# response = chatbot._get_chatgpt_response("Qual è stato l'andamento trimestrale nel 2022")
# if isinstance(response, Image.Image):
#     response.show()
# else:
#     print(response)





        
        
        
        

#Funzione da ottimizzare per separare in modo più netto le query legate agli andamenti mensili da quelle legate agli andamenti trimestrali
    # def _get_chatgpt_response(self, prompt, chat_history=[]):
    #     andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
    #     previsioni_obj = Forecast(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")

    #     if "andamento trimestrale" in prompt.lower():
    #         reply, image = andamenti_obj.plot_andamenti_trimestrali()
    #         grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #         fatturato_per_annualita = {}
    #         #RETTIFICHE#INIZIO
    #         max_fatturato_value = float('-inf')
    #         max_fatturato_year = None
    #         max_fatturato_trimester = None

    #         min_fatturato_value = float('inf')
    #         min_fatturato_year = None
    #         min_fatturato_trimester = None
    #         #FINE
    #         for name, group in grouped:
    #             group['Trimestre'] = group['Data fattura'].dt.quarter
    #             series = group.groupby('Trimestre')['Totale'].sum()
    #             #RETTIFICHE#INIZIO
    #             if series.max() > max_fatturato_value:
    #                 max_fatturato_value = series.max()
    #                 max_fatturato_year = name
    #                 max_fatturato_trimester = series.idxmax()

    #             if series.min() < min_fatturato_value:
    #                 min_fatturato_value = series.min()
    #                 min_fatturato_year = name
    #                 min_fatturato_trimester = series.idxmin()
    #                 #FINE

    #             fatturato_per_annualita[name] = {
    #                 "fatturato_totale": series.sum(),
    #                 "fatturato_max": series.max(),
    #                 "fatturato_min": series.min()
    #             }
    #         metadata = {
    #             "fatturato_per_annualita": fatturato_per_annualita,
    #             #RETTIFICHE INIZIO
    #             "max_fatturato": {
    #             "year": int(max_fatturato_year),
    #             "trimester": int(max_fatturato_trimester),
    #             "value": float(max_fatturato_value)
    #         },
    #             "min_fatturato": {
    #                 "year": int(min_fatturato_year),
    #                 "trimester": int(min_fatturato_trimester),
    #                 "value": float(min_fatturato_value)
    #             }


    #         }

    #         # Memorizza l'immagine e i metadati nella chat history
    #         output = io.BytesIO()
    #         image.save(output, format='PNG')
    #         self.env['chat.history'].create({
    #                 'channel_id': self.id,
    #                 'role': 'assistant',
    #                 'content': 'Vedi immagine allegata',
    #                 'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #                 'image_metadata': metadata,
    #                 'chart_type': 'trimestrial'
    #             })

    #         trimestral_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Trimestrial Chart'>"
    #         return trimestral_html
    #     last_image_metadata_trimestral = self.env['chat.history'].search(
    #         [('channel_id', '=', self.id), ('content', '=', "Ecco a te l'andamento trimestrale richiesto"),('image_data', '!=', False), ('chart_type', '=', 'trimestrial')],
    #         order='id desc', limit=1).image_metadata
    #     # last_image_metadata_trimestral = self.env['chat.history'].search([('channel_id', '=', self.id), ('image_data', '!=', False)], order='id desc', limit=1).image_metadata
    #     if last_image_metadata_trimestral and "fatturato totale" in prompt.lower():
    #         fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata_trimestral['fatturato_per_annualita'].items()}  
    #         return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata_trimestral['fatturato_per_annualita']}"
    #     if last_image_metadata_trimestral and "massimo fatturato" and "fatturato massimo" in prompt.lower():
    #         max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
    #         fatturato_max_global = max(max_values)
    #         year = last_image_metadata_trimestral['max_fatturato']['year']
    #         trimester = last_image_metadata_trimestral['max_fatturato']['trimester']
    #         return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

    #     if last_image_metadata_trimestral and "minimo fatturato" and "fatturato minimo" in prompt.lower():
    #         min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
    #         fatturato_min_global = min(min_values)
    #         year = last_image_metadata_trimestral['min_fatturato']['year']
    #         trimester = last_image_metadata_trimestral['min_fatturato']['trimester']
    #         return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."
        

    #     elif "andamento mensile" in prompt.lower():
    #         reply, image = andamenti_obj.plot_andamenti_mensili()
    #         grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #         fatturato_per_annualita = {}
            
    #         max_fatturato_value = float('-inf')
    #         max_fatturato_year = None
    #         max_fatturato_month = None

    #         min_fatturato_value = float('inf')
    #         min_fatturato_year = None
    #         min_fatturato_month = None
            
    #         for name, group in grouped:
    #             group = group.copy()
    #             group['Mese'] = group['Data fattura'].dt.month
    #             series = group.groupby('Mese')['Totale'].sum()
                
    #             if series.max() > max_fatturato_value:
    #                 max_fatturato_value = series.max()
    #                 max_fatturato_year = name
    #                 max_fatturato_month = series.idxmax()

    #             if series.min() < min_fatturato_value:
    #                 min_fatturato_value = series.min()
    #                 min_fatturato_year = name
    #                 min_fatturato_month = series.idxmin()

    #             fatturato_per_annualita[name] = {
    #                 "fatturato_totale": series.sum(),
    #                 "fatturato_max": series.max(),
    #                 "fatturato_min": series.min()
    #             }

    #         metadata = {
    #             "fatturato_per_annualita": fatturato_per_annualita,
    #             "max_fatturato": {
    #                 "year": int(max_fatturato_year),
    #                 "month": int(max_fatturato_month),
    #                 "value": float(max_fatturato_value)
    #             },
    #             "min_fatturato": {
    #                 "year": int(min_fatturato_year),
    #                 "month": int(min_fatturato_month),
    #                 "value": float(min_fatturato_value)
    #             }
    #         }

    #         # Memorizza l'immagine e i metadati nella chat history
    #         output = io.BytesIO()
    #         image.save(output, format='PNG')
    #         self.env['chat.history'].create({
    #                 'channel_id': self.id,
    #                 'role': 'assistant',
    #                 'content': 'Vedi immagine allegata',
    #                 'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #                 'image_metadata': metadata,
    #                 'chart_type': 'monthly'
    #             })

    #         mensile_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Monthly Chart'>"
    #         return mensile_html
        
    #     # last_image_metadata_mensile = self.env['chat.history'].search([('channel_id', '=', self.id), ('image_data', '!=', False)], order='id desc', limit=1).image_metadata
    #     last_image_metadata_mensile = self.env['chat.history'].search(
    #         [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'monthly')],
    #         order='id desc', limit=1).image_metadata
    #     if last_image_metadata_mensile and "fatturato totale" in prompt.lower():
    #         fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata_mensile['fatturato_per_annualita'].items()}  
    #         return f"I fatturati totali per ciascun anno e con relativi picchi mensili sono stati i seguenti: {last_image_metadata_mensile['fatturato_per_annualita']}"
   

    #     if last_image_metadata_mensile and (("massimo fatturato" in prompt.lower()) or ("fatturato massimo" in prompt.lower())):
    #         max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_mensile['fatturato_per_annualita'].values()]
    #         fatturato_max_global = max(max_values)
    #         year = last_image_metadata_mensile['max_fatturato']['year']
    #         month = last_image_metadata_mensile['max_fatturato']['month']
    #         return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {month}° mese dell'anno {year}."

    #     if last_image_metadata_mensile and (("minimo fatturato" in prompt.lower()) or ("fatturato minimo" in prompt.lower())):
    #         min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_mensile['fatturato_per_annualita'].values()]
    #         fatturato_min_global = min(min_values)
    #         year = last_image_metadata_mensile['min_fatturato']['year']
    #         month = last_image_metadata_mensile['min_fatturato']['month']
    #         return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {month}° mese dell'anno {year}."

   
        
        
        # elif "previsioni mensili" in prompt.lower():
        #     reply, image= previsioni_obj.plot_previsioni_mensili()
        #     output= io.BytesIO()
        #     image.save(output, format='PNG')
        #     b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

        #     img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Monthly Forecast'>"

        #     return img_html
        # elif "previsioni trimestrali" in prompt.lower():
        #     reply, image= previsioni_obj.plot_previsioni_trimestrali()
        #     output= io.BytesIO()
        #     image.save(output, format='PNG')
        #     b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

        #     img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Trimestral Forecast'>"

        #     return img_html
    
    
        # ICP = self.env['ir.config_parameter'].sudo()
        # openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
        # gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
        # gpt_model = 'gpt-3.5-turbo'
        # try:
        #     if gpt_model_id:
        #         gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
        # except Exception as ex:
        #     gpt_model = 'gpt-3.5-turbo'
        #     pass
        
        # user_message = {"role": "user", "content": prompt}
        
        # chat_history.append(user_message)
        
        # total_tokens = sum(len(msg["content"].split()) for msg in chat_history)  # this is a naive token estimate by counting words
        
        # # safety_margin = 500
        
        # max_response_tokens = 1500 - total_tokens
        
        # while max_response_tokens <= 0:
        #     removed_message = chat_history.pop(0)  # remove the oldest message
        #     total_tokens -= len(removed_message["content"].split())  # update total_tokens
        #     max_response_tokens = 1500 - total_tokens
        # try:
        #     chat = openai.ChatCompletion.create(
        #     model=gpt_model,
        #     messages=chat_history,
        #     temperature=0.6,
        #     max_tokens=max_response_tokens,  # the remaining tokens available
        # )
        #     assistant_reply = chat.choices[0].message['content']
            
        #     chat_history.append({"role": "assistant", "content": assistant_reply})
            
        #     return assistant_reply
        # except Exception as e:
        #     print("An error occurred:", e)
        #     raise UserError(_("An error occurred: %s") % e)
            
#TENTATIVO DI OTTENERE ALTRE INFORMAZIONI DAGLI ANDAMENTI MENSILI (FATT.TOTALE, MASSIMO, MINIMO)
# import pandas as pd
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# import io
# from PIL import Image
# import openai
# import base64
# from odoo import api, fields, models
# from odoo.exceptions import UserError
# from odoo.tools.translate import _

# class Andamenti:
#     def __init__(self, file_path):
#         self.tabella = pd.read_csv(file_path, header=None,
#                                    names=["Cliente", "Data fattura", "Numero", "Addetto vendite", "Data scadenza",
#                                          "Documento origine", "Insoluta", "Imponibile", "Imposta", "Totale",
#                                          "Importo dovuto", "Stato e-fattura", "Stato"])
#         self.tabella["Data fattura"] = pd.to_datetime(self.tabella["Data fattura"])

#     def plot_andamenti(self, frequency, title):
#         grouped = self.tabella.groupby(self.tabella['Data fattura'].dt.year)
#         plt.figure(figsize=(12, 6))

#         for name, group in grouped:
#             group['Mese'] = group['Data fattura'].dt.month
#             series = group.groupby('Mese')['Totale'].sum()
#             plt.plot(series.index, series, label=f'Dati {name}')

#         month_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#         plt.xticks(list(range(1, 13)), month_names, rotation=45)

#         plt.xlabel('Mese')
#         plt.ylabel('Totale')
#         plt.title(title)
#         plt.legend()
#         plt.grid(True)
        
#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         andamenti_img = Image.open(output)
#         return f"Andamento storico {frequency}:", andamenti_img

#     def plot_andamenti_trimestrali_per_annualita(self):
#         grouped = self.tabella.groupby(self.tabella['Data fattura'].dt.year)
#         plt.figure(figsize=(12, 6))

#         for name, group in grouped:
#             group['Trimestre'] = group['Data fattura'].dt.quarter
#             series = group.groupby('Trimestre')['Totale'].sum()
#             plt.plot(series.index, series, label=f'Dati {name}')

#         trimestre_names = ['Q1', 'Q2', 'Q3', 'Q4']
#         plt.xticks(list(range(1, 5)), trimestre_names, rotation=45)

#         plt.xlabel('Trimestre')
#         plt.ylabel('Totale')
#         plt.title('Andamenti Trimestrali per Annualità')
#         plt.legend()
#         plt.grid(True)
        
#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         andamenti_img = Image.open(output)
#         return "Andamento storico trimestrale per annualità:", andamenti_img

#     def plot_andamenti_mensili(self):
#         return self.plot_andamenti('M', 'Andamenti mensili')

#     def plot_andamenti_trimestrali(self):
#         return self.plot_andamenti_trimestrali_per_annualita()

# class ChatHistory(models.Model):
#     _name = 'chat.history'
#     channel_id = fields.Many2one('mail.channel', required=True, ondelete='cascade')
#     role = fields.Selection([('user', 'User'), ('assistant', 'Assistant')], required=True)
#     content = fields.Text(required=True)
#     image_data = fields.Binary('Image')
#     image_filename = fields.Char()
#     metadata = fields.Serialized()
#     image_metadata = fields.Serialized()
#     chart_type = fields.Selection([('trimestrial', 'Trimestrial'), ('monthly', 'Monthly')], string='Chart Type')
    
#     @api.model
#     def approximate_token_count(self, text):
#         return len(text.split())

#     @api.model
#     def _notify_thread(self, message, msg_vals=False, **kwargs):
#         rdata = super(ChatHistory, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
#         chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
#         user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
#         partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
#         author_id = msg_vals.get('author_id')
#         chatgpt_name = str(partner_chatgpt.name or '') + ', '
#         prompt = msg_vals.get('body')
        
#         if not prompt:
#             return rdata
#         openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
#         Partner = self.env['res.partner']
#         partner_name = ''
#         if author_id:
#             partner_id = Partner.browse(author_id)
#             if partner_id:
#                 partner_name = partner_id.name
#         if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         return rdata


# class Channel(models.Model):
#     _inherit = 'mail.channel'
    
#     @api.model
#     def approximate_token_count(self, text):
#         return len(text.split())
    
#     @api.model
#     def _notify_thread(self, message, msg_vals=False, **kwargs):
#         rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
#         chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
#         user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
#         partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
#         author_id = msg_vals.get('author_id')
#         chatgpt_name = str(partner_chatgpt.name or '') + ', '
#         prompt = msg_vals.get('body')
        
#         if not prompt:
#             return rdata
#         openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
#         Partner = self.env['res.partner']
#         partner_name = ''
#         if author_id:
#             partner_id = Partner.browse(author_id)
#             if partner_id:
#                 partner_name = partner_id.name
#         if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         return rdata
    
#     def _get_chatgpt_response(self, prompt, chat_history=[]):
#         andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")

#         if "andamento trimestrale" in prompt.lower():
#             if "fatturato totale" in prompt.lower():
#                 return self.generate_total_fatturato_response("trimestrial", andamenti_obj)
#             elif "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
#                 return self.generate_max_fatturato_response("trimestrial", andamenti_obj)
#             elif "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
#                 return self.generate_min_fatturato_response("trimestrial", andamenti_obj)

#         elif "andamento mensile" in prompt.lower():
#             if "fatturato totale" in prompt.lower():
#                 return self.generate_total_fatturato_response("monthly", andamenti_obj)
#             elif "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
#                 return self.generate_max_fatturato_response("monthly", andamenti_obj)
#             elif "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
#                 return self.generate_min_fatturato_response("monthly", andamenti_obj)

#         last_image_metadata = self.env['chat.history'].search([
#             ('channel_id', '=', self.id),
#             ('image_data', '!=', False),
#             ('chart_type', '=', 'trimestrial')
#         ], order='id desc', limit=1).image_metadata

#         if last_image_metadata:
#             if last_image_metadata.get("chart_type") == "trimestrial":
#                 if "fatturato totale" in prompt.lower():
#                     fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata['fatturato_per_annualita'].items()}  
#                     return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata['fatturato_per_annualita']}"
                
#                 if "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
#                     max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
#                     fatturato_max_global = max(max_values)
#                     year = last_image_metadata['max_fatturato']['year']
#                     trimester = last_image_metadata['max_fatturato']['trimester']
#                     return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."
                
#                 if "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
#                     min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
#                     fatturato_min_global = min(min_values)
#                     year = last_image_metadata['min_fatturato']['year']
#                     trimester = last_image_metadata['min_fatturato']['trimester']
#                     return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

#         ICP = self.env['ir.config_parameter'].sudo()
#         openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
#         gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
#         gpt_model = 'gpt-3.5-turbo'
#         try:
#             if gpt_model_id:
#                 gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
#         except Exception as ex:
#             gpt_model = 'gpt-3.5-turbo'
#             pass
        
#         user_message = {"role": "user", "content": prompt}
        
#         chat_history.append(user_message)
        
#         total_tokens = sum(len(msg["content"].split()) for msg in chat_history)  # this is a naive token estimate by counting words
        
#         # safety_margin = 500
        
#         max_response_tokens = 1500 - total_tokens
        
#         while max_response_tokens <= 0:
#             removed_message = chat_history.pop(0)  # remove the oldest message
#             total_tokens -= len(removed_message["content"].split())  # update total_tokens
#             max_response_tokens = 1500 - total_tokens
#         try:
#             chat = openai.ChatCompletion.create(
#             model=gpt_model,
#             messages=chat_history,
#             temperature=0.6,
#             max_tokens=max_response_tokens,  # the remaining tokens available
#         )
#             assistant_reply = chat.choices[0].message['content']
            
#             chat_history.append({"role": "assistant", "content": assistant_reply})
            
#             return assistant_reply
#         except Exception as e:
#             print("An error occurred:", e)
#             raise UserError(_("An error occurred: %s") % e)
    
    
#     def generate_max_fatturato_response(self, chart_type, andamenti_obj):
#         if chart_type == "trimestrial":
#             max_fatturato = andamenti_obj.get_max_fatturato("trimestrial")
#             year = max_fatturato["year"]
#             trimester = max_fatturato["trimester"]
#             value = max_fatturato["value"]
#             return f"Il fatturato massimo del valore di {value} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

#         elif chart_type == "monthly":
#             max_fatturato = andamenti_obj.get_max_fatturato("monthly")
#             year = max_fatturato["year"]
#             month = max_fatturato["month"]
#             value = max_fatturato["value"]
#             return f"Il fatturato massimo del valore di {value} è stato conseguito nel mese {month} dell'anno {year}."

    

#     def generate_min_fatturato_response(self, chart_type, andamenti_obj):
#         if chart_type == "trimestrial":
#             min_fatturato = andamenti_obj.get_min_fatturato("trimestrial")
#             year = min_fatturato["year"]
#             trimester = min_fatturato["trimester"]
#             value = min_fatturato["value"]
#             return f"Il fatturato minimo del valore di {value} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

#         elif chart_type == "monthly":
#             min_fatturato = andamenti_obj.get_min_fatturato("monthly")
#             year = min_fatturato["year"]
#             month = min_fatturato["month"]
#             value = min_fatturato["value"]
#             return f"Il fatturato minimo del valore di {value} è stato conseguito nel mese {month} dell'anno {year}."
#     def _get_response_message(self, andamenti_obj):
#         trimestrial_plot_img = andamenti_obj.plot_andamenti_trimestrali_per_annualita()
#         monthly_plot_img = andamenti_obj.plot_andamenti_mensili()
#         total_fatturato = self.generate_total_fatturato_response("trimestrial", andamenti_obj)
#         max_fatturato = self.generate_max_fatturato_response("trimestrial", andamenti_obj)
#         min_fatturato = self.generate_min_fatturato_response("trimestrial", andamenti_obj)

#         trimestrial_plot_base64 = base64.b64encode(trimestrial_plot_img[1].tobytes()).decode("utf-8")
#         monthly_plot_base64 = base64.b64encode(monthly_plot_img[1].tobytes()).decode("utf-8")

#         trimestrial_trend_response = f"Here's the trimestrial trend:\n{trimestrial_plot_img[0]}\n[Image](data:image/png;base64,{trimestrial_plot_base64})"
#         monthly_trend_response = f"Here's the monthly trend:\n{monthly_plot_img[0]}\n[Image](data:image/png;base64,{monthly_plot_base64})"
#         total_fatturato_response = f"Total Fatturato Response: {total_fatturato}"
#         max_fatturato_response = f"Maximum Fatturato Response: {max_fatturato}"
#         min_fatturato_response = f"Minimum Fatturato Response: {min_fatturato}"

#         final_response = f"{trimestrial_trend_response}\n\n{monthly_trend_response}\n\n{total_fatturato_response}\n\n{max_fatturato_response}\n\n{min_fatturato_response}"

#         return final_response





    # def _get_chatgpt_response(self, prompt, chat_history=[]):
    #     andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
    #     # previsioni_obj = Forecast(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")

    #     if "andamento trimestrale" in prompt.lower():
    #         reply, image = andamenti_obj.plot_andamenti_trimestrali()
    #         grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #         fatturato_per_annualita = {}
    #         #RETTIFICHE#INIZIO
    #         max_fatturato_value = float('-inf')
    #         max_fatturato_year = None
    #         max_fatturato_trimester = None

    #         min_fatturato_value = float('inf')
    #         min_fatturato_year = None
    #         min_fatturato_trimester = None
    #         #FINE
    #         for name, group in grouped:
    #             group['Trimestre'] = group['Data fattura'].dt.quarter
    #             series = group.groupby('Trimestre')['Totale'].sum()
    #             #RETTIFICHE#INIZIO
    #             if series.max() > max_fatturato_value:
    #                 max_fatturato_value = series.max()
    #                 max_fatturato_year = name
    #                 max_fatturato_trimester = series.idxmax()

    #             if series.min() < min_fatturato_value:
    #                 min_fatturato_value = series.min()
    #                 min_fatturato_year = name
    #                 min_fatturato_trimester = series.idxmin()
    #                 #FINE

    #             fatturato_per_annualita[name] = {
    #                 "fatturato_totale": series.sum(),
    #                 "fatturato_max": series.max(),
    #                 "fatturato_min": series.min()
    #             }
    #         metadata = {
    #             "fatturato_per_annualita": fatturato_per_annualita,
    #             #RETTIFICHE INIZIO
    #             "max_fatturato": {
    #             "year": int(max_fatturato_year),
    #             "trimester": int(max_fatturato_trimester),
    #             "value": float(max_fatturato_value)
    #         },
    #             "min_fatturato": {
    #                 "year": int(min_fatturato_year),
    #                 "trimester": int(min_fatturato_trimester),
    #                 "value": float(min_fatturato_value)
    #             }


    #         }

    #         # Memorizza l'immagine e i metadati nella chat history
    #         output = io.BytesIO()
    #         image.save(output, format='PNG')
    #         self.env['chat.history'].create({
    #             'channel_id': self.id,
    #             'role': 'assistant',
    #             'content': 'Vedi immagine allegata',
    #             'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #             'image_metadata': metadata,
    #             'chart_type': 'trimestrial'
    #         })

    #         trimestral_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Trimestrial Chart'>"
    #         return trimestral_html
    #     last_image_metadata = self.env['chat.history'].search([
    #         ('channel_id', '=', self.id),
    #         ('image_data', '!=', False),
    #         ('chart_type', '=', 'trimestrial')
    #     ], order='id desc', limit=1).image_metadata



        
    #     if "andamento mensile" in prompt.lower():
    #         reply, image = andamenti_obj.plot_andamenti_mensili()
    #         grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #         fatturato_per_annualita = {}
            
    #         max_fatturato_value = float('-inf')
    #         max_fatturato_year = None
    #         max_fatturato_month = None

    #         min_fatturato_value = float('inf')
    #         min_fatturato_year = None
    #         min_fatturato_month = None
            
    #         for name, group in grouped:
    #             group['Mese'] = group['Data fattura'].dt.month
    #             series_monthly = group.groupby('Mese')['Totale'].sum()
                
    #             if series_monthly.max() > max_fatturato_value:
    #                 max_fatturato_value = series_monthly.max()
    #                 max_fatturato_year = name
    #                 max_fatturato_month = series_monthly.idxmax()

    #             if series_monthly.min() < min_fatturato_value:
    #                 min_fatturato_value = series_monthly.min()
    #                 min_fatturato_year = name
    #                 min_fatturato_month = series_monthly.idxmin()
    #                 #FINE

    #             fatturato_per_annualita[name] = {
    #                 "fatturato_totale": series_monthly.sum(),
    #                 "fatturato_max": series_monthly.max(),
    #                 "fatturato_min": series_monthly.min()
    #             }
    #         metadata = {
    #             "fatturato_per_annualita": fatturato_per_annualita,
    #             #RETTIFICHE INIZIO
    #             "max_fatturato": {
    #             "year": int(max_fatturato_year),
    #             "month": int(max_fatturato_month),
    #             "value": float(max_fatturato_value)
    #         },
    #             "min_fatturato": {
    #                 "year": int(min_fatturato_year),
    #                 "month": int(min_fatturato_month),
    #                 "value": float(min_fatturato_value)
    #             }


    #         }

    #         # Memorizza l'immagine e i metadati nella chat history
    #         output = io.BytesIO()
    #         image.save(output, format='PNG')
    #         self.env['chat.history'].create({
    #             'channel_id': self.id,
    #             'role': 'assistant',
    #             'content': 'Vedi immagine allegata',
    #             'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #             'image_metadata': metadata,
    #             'chart_type': 'monthly'
    #         })

    #         monthly_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Monthly Chart'>"
    #         return monthly_html
    #     last_image_metadata = self.env['chat.history'].search([
    #         ('channel_id', '=', self.id),
    #         ('image_data', '!=', False),
    #         ('chart_type', '=', 'monthly')
    #     ], order='id desc', limit=1).image_metadata
        
    #     if last_image_metadata:
    # # Query per l'andamento trimestrale

    #         # if last_image_metadata["chart_type"] == "trimestrial":
    #         #possibile rettifica per dopo
    #         if last_image_metadata.get("chart_type") == "trimestrial":
    

                
    #             if "fatturato totale" in prompt.lower():
    #                 fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata['fatturato_per_annualita'].items()}  
    #                 return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata['fatturato_per_annualita']}"
                
    #             if "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
    #                 max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
    #                 fatturato_max_global = max(max_values)
    #                 year = last_image_metadata['max_fatturato']['year']
    #                 trimester = last_image_metadata['max_fatturato']['trimester']
    #                 return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

    #             if "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
    #                 min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
    #                 fatturato_min_global = min(min_values)
    #                 year = last_image_metadata['min_fatturato']['year']
    #                 trimester = last_image_metadata['min_fatturato']['trimester']
    #                 return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

    #         # Query per l'andamento mensile
    #         elif last_image_metadata.get("chart_type") == "monthly":
    #             if "fatturato totale" in prompt.lower():
    #                 fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata['fatturato_per_annualita'].items()}  
    #                 return f"I fatturati totali per ciascun anno e con relativi picchi mensili sono stati i seguenti: {last_image_metadata['fatturato_per_annualita']}"
                
    #             if "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
    #                 max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
    #                 fatturato_max_global = max(max_values)
    #                 year = last_image_metadata['max_fatturato']['year']
    #                 month = last_image_metadata['max_fatturato']['month']
    #                 return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {month}° mese dell'anno {year}."

    #             if "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
    #                 min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
    #                 fatturato_min_global = min(min_values)
    #                 year = last_image_metadata['min_fatturato']['year']
    #                 month = last_image_metadata['min_fatturato']['month']
    #                 return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {month}° mese dell'anno {year}."
    #             # return img_html
            
    #     ICP = self.env['ir.config_parameter'].sudo()
    #     openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
    #     gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
    #     gpt_model = 'gpt-3.5-turbo'
    #     try:
    #         if gpt_model_id:
    #             gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
    #     except Exception as ex:
    #         gpt_model = 'gpt-3.5-turbo'
    #         pass
        
    #     user_message = {"role": "user", "content": prompt}
        
    #     chat_history.append(user_message)
        
    #     total_tokens = sum(len(msg["content"].split()) for msg in chat_history)  # this is a naive token estimate by counting words
        
    #     # safety_margin = 500
        
    #     max_response_tokens = 1500 - total_tokens
        
    #     while max_response_tokens <= 0:
    #         removed_message = chat_history.pop(0)  # remove the oldest message
    #         total_tokens -= len(removed_message["content"].split())  # update total_tokens
    #         max_response_tokens = 1500 - total_tokens
    #     try:
    #         chat = openai.ChatCompletion.create(
    #         model=gpt_model,
    #         messages=chat_history,
    #         temperature=0.6,
    #         max_tokens=max_response_tokens,  # the remaining tokens available
    #     )
    #         assistant_reply = chat.choices[0].message['content']
            
    #         chat_history.append({"role": "assistant", "content": assistant_reply})
            
    #         return assistant_reply
    #     except Exception as e:
    #         print("An error occurred:", e)
    #         raise UserError(_("An error occurred: %s") % e)
#Questo è importante
        # elif "previsioni mensili" in prompt.lower():
        #     reply, image= previsioni_obj.plot_previsioni_mensili()
        #     output= io.BytesIO()
        #     image.save(output, format='PNG')
        #     b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

        #     img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Monthly Forecast'>"

        #     return img_html
        # elif "previsioni trimestrali" in prompt.lower():
        #     reply, image= previsioni_obj.plot_previsioni_trimestrali()
        #     output= io.BytesIO()
        #     image.save(output, format='PNG')
        #     b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

        #     img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Trimestral Forecast'>"

        #     return img_html
    

            
            # Devi implementare una logica simile a quella sopra ma per l'andamento mensile. 
        # Ad esempio, potresti avere delle query simili ma che parlano di mesi invece che di trimestri.
        # ...

        # if last_image_metadata and "fatturato totale" in prompt.lower():
        #     fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata['fatturato_per_annualita'].items()}  
        #     return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata['fatturato_per_annualita']}"
        # if last_image_metadata and "massimo fatturato" and "fatturato massimo" in prompt.lower():
        #     max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
        #     fatturato_max_global = max(max_values)
        #     year = last_image_metadata['max_fatturato']['year']
        #     trimester = last_image_metadata['max_fatturato']['trimester']
        #     return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

        # if last_image_metadata and "minimo fatturato" and "fatturato minimo" in prompt.lower():
        #     min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata['fatturato_per_annualita'].values()]
        #     fatturato_min_global = min(min_values)
        #     year = last_image_metadata['min_fatturato']['year']
        #     trimester = last_image_metadata['min_fatturato']['trimester']
        #     return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."



#SUGGERIMENTI PER RETTIFICHE
# import pandas as pd
# import matplotlib.pyplot as plt
# import io
# from PIL import Image
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# import openai
# import base64
# from odoo import api, fields, models
# from odoo.exceptions import UserError
# from odoo.tools.translate import _

# class Andamenti:
#     def __init__(self, file_path):
#         self.tabella = pd.read_csv(file_path, header=None,
#                                    names=["Cliente", "Data fattura", "Numero", "Addetto vendite", "Data scadenza",
#                                          "Documento origine", "Insoluta", "Imponibile", "Imposta", "Totale",
#                                          "Importo dovuto", "Stato e-fattura", "Stato"])
#         self.tabella["Data fattura"] = pd.to_datetime(self.tabella["Data fattura"])

#     def plot_andamenti(self, frequency, title):
#         grouped = self.tabella.groupby(self.tabella['Data fattura'].dt.year)
#         plt.figure(figsize=(12, 6))

#         for name, group in grouped:
#             # Creiamo una nuova colonna "Mese" per estrarre solo il mese dalla data della fattura
#             group['Mese'] = group['Data fattura'].dt.month
#             series = group.groupby('Mese')['Totale'].sum()

#             # Grafichiamo i dati
#             plt.plot(series.index, series, label=f'Dati {name}')

#         # Impostiamo le etichette dell'asse x come i nomi dei mesi
#         month_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#         plt.xticks(list(range(1, 13)), month_names, rotation=45)

#         plt.xlabel('Mese')
#         plt.ylabel('Totale')
#         plt.title(title)
#         plt.legend()
#         plt.grid(True)
        
#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         andamenti_img = Image.open(output)
#         return f"Andamento storico {frequency}:", andamenti_img
#     def plot_andamenti_trimestrali_per_annualita(self):
#         grouped = self.tabella.groupby(self.tabella['Data fattura'].dt.year)
#         plt.figure(figsize=(12, 6))

#         for name, group in grouped:
#             # Creiamo una nuova colonna "Trimestre" per estrarre il trimestre dalla data della fattura
#             group['Trimestre'] = group['Data fattura'].dt.quarter
#             series = group.groupby('Trimestre')['Totale'].sum()

#             # Grafichiamo i dati
#             plt.plot(series.index, series, label=f'Dati {name}')

#         # Impostiamo le etichette dell'asse x come i numeri dei trimestri
#         trimestre_names = ['Q1', 'Q2', 'Q3', 'Q4']
#         plt.xticks(list(range(1, 5)), trimestre_names, rotation=45)

#         plt.xlabel('Trimestre')
#         plt.ylabel('Totale')
#         plt.title('Andamenti Trimestrali per Annualità')
#         plt.legend()
#         plt.grid(True)
        
#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         andamenti_img = Image.open(output)# 
#         return "Andamento storico trimestrale per annualità:", andamenti_img


#     def plot_andamenti_mensili(self):
#         return self.plot_andamenti('M', 'Andamenti mensili')

#     def plot_andamenti_trimestrali(self):
#         return self.plot_andamenti_trimestrali_per_annualita()
# class Forecast:

#     def __init__(self, file_path):
#         self.tabella = pd.read_csv(file_path, header=None,
#                                    names=["Cliente", "Data fattura", "Numero", "Addetto vendite", "Data scadenza",
#                                          "Documento origine", "Insoluta", "Imponibile", "Imposta", "Totale",
#                                          "Importo dovuto", "Stato e-fattura", "Stato"])
#         self.tabella["Data fattura"] = pd.to_datetime(self.tabella["Data fattura"])

#     def get_min_value(self):
#         return self.tabella["Totale"].min()

#     def plot_forecast(self, frequency, title, steps):
#         series = self.tabella.set_index("Data fattura")["Totale"].resample(frequency).sum()

#         train_data = series[:'2023']
#         test_data = series['2024':'2026']

#         model = SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
#         model_fit = model.fit()

#         forecast = model_fit.get_forecast(steps=steps)
#         forecast_values = forecast.predicted_mean
#         conf_int = forecast.conf_int()
#         forecast_data = pd.DataFrame({
#             'Data': forecast_values.index,
#             'Previsione': forecast_values.values,
#             'Intervallo di confidenza (inferiore)': conf_int.iloc[:, 0].values,
#             'Intervallo di confidenza (superiore)': conf_int.iloc[:, 1].values
#         })

#         plt.plot(train_data.index, train_data, label='Dati storici')
#         plt.plot(test_data.index, test_data, label='Dati di test')
#         plt.plot(forecast_data['Data'], forecast_data['Previsione'], label='Previsioni')
#         plt.fill_between(forecast_data['Data'], forecast_data['Intervallo di confidenza (inferiore)'],
#                          forecast_data['Intervallo di confidenza (superiore)'], alpha=0.2, color='gray',
#                          label='Intervallo di confidenza')
#         plt.xlabel('Data')
#         plt.ylabel('Totale')
#         plt.title(title)
#         plt.legend()
#         plt.xticks(rotation=45)

#         output = io.BytesIO()
#         plt.savefig(output, format="png")
#         plt.close()
#         output.seek(0)
#         forecast_img = Image.open(output)

#         return f"Ecco l'andamento {frequency}:", forecast_img

#     def plot_previsioni_mensili(self):
#         return self.plot_forecast('M', 'Previsioni mensili', 36)

#     def plot_previsioni_trimestrali(self):
#         return self.plot_forecast('Q', 'Previsioni trimestrali', 14)

# class ChatHistory(models.Model):
#     _name = 'chat.history'
#     channel_id = fields.Many2one('mail.channel', required=True, ondelete='cascade')
#     role = fields.Selection([('user', 'User'), ('assistant', 'Assistant')], required=True)
#     content = fields.Text(required=True)
#     image_data = fields.Binary('Image')  # Aggiunto per memorizzare l'immagine
#     image_filename = fields.Char()
#     metadata = fields.Serialized()
#     image_metadata = fields.Serialized()
    
#     chart_type = fields.Selection([('trimestrial', 'Trimestrial'), ('monthly', 'Monthly')], string="Chart Type")
    
#     # @api.model
#     # def approximate_token_count(self, text):
#     #     return len(text.split())

#     @api.model
#     def _notify_thread(self, message, msg_vals=False, **kwargs):
#         rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
#         chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
#         user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
#         partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
#         author_id = msg_vals.get('author_id')
#         chatgpt_name = str(partner_chatgpt.name or '') + ', '
#         prompt = msg_vals.get('body')
        
#         if not prompt:
#             return rdata
#         openai.api_key = self.env['ir.config_parameter'].sudo().get_param('is_chatgpt_integration.openapi_api_key')
#         Partner = self.env['res.partner']
#         partner_name = ''
#         if author_id:
#             partner_id = Partner.browse(author_id)
#             if partner_id:
#                 partner_name = partner_id.name
#         if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
#             try:
#                 res = self._get_chatgpt_response(prompt=prompt)
#                 chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
#             except Exception as e:
#                 raise UserError(_(e))

#         return rdata



# #codice da qui sono partito per gestire le richieste separate di ottenimento dei#Fatturati totali, massimo, minimo legati all'andamento mensile
# #Fatturati totali, massimo, minimo legati all'andamento trimestrale
# class Channel(models.Model):
#     _inherit = 'mail.channel'

#     @api.model
#     def approximate_token_count(self, text):
#         return len(text.split())


#     def _get_chatgpt_response(self, prompt, chat_history=[]):
#         andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
#         previsioni_obj = Forecast(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")

#         if "andamento trimestrale" in prompt.lower():
#             reply, image = andamenti_obj.plot_andamenti_trimestrali()
#             grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
#             fatturato_per_annualita = {}
#             #RETTIFICHE#INIZIO
#             max_fatturato_value = float('-inf')
#             max_fatturato_year = None
#             max_fatturato_trimester = None

#             min_fatturato_value = float('inf')
#             min_fatturato_year = None
#             min_fatturato_trimester = None
#             #FINE
#             for name, group in grouped:
#                 group['Trimestre'] = group['Data fattura'].dt.quarter
#                 series = group.groupby('Trimestre')['Totale'].sum()
#                 #RETTIFICHE#INIZIO
#                 if series.max() > max_fatturato_value:
#                     max_fatturato_value = series.max()
#                     max_fatturato_year = name
#                     max_fatturato_trimester = series.idxmax()

#                 if series.min() < min_fatturato_value:
#                     min_fatturato_value = series.min()
#                     min_fatturato_year = name
#                     min_fatturato_trimester = series.idxmin()
#                     #FINE

#                 fatturato_per_annualita[name] = {
#                     "fatturato_totale": series.sum(),
#                     "fatturato_max": series.max(),
#                     "fatturato_min": series.min()
#                 }
#             metadata = {
#                 "fatturato_per_annualita": fatturato_per_annualita,
#                 #RETTIFICHE INIZIO
#                 "max_fatturato": {
#                 "year": int(max_fatturato_year),
#                 "trimester": int(max_fatturato_trimester),
#                 "value": float(max_fatturato_value)
#             },
#                 "min_fatturato": {
#                     "year": int(min_fatturato_year),
#                     "trimester": int(min_fatturato_trimester),
#                     "value": float(min_fatturato_value)
#                 }


#             }

#             # Memorizza l'immagine e i metadati nella chat history
#             output = io.BytesIO()
#             image.save(output, format='PNG')
#             self.env['chat.history'].create({
#                     'channel_id': self.id,
#                     'role': 'assistant',
#                     'content': 'Vedi immagine allegata',
#                     'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
#                     'image_metadata': metadata,
#                     'chart_type': 'trimestrial'
#                 })

#             trimestral_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Trimestrial Chart'>"
#             return trimestral_html
#         last_image_metadata_trimestral = self.env['chat.history'].search(
#             [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'trimestrial')],
#             order='id desc', limit=1).image_metadata
#         # last_image_metadata_trimestral = self.env['chat.history'].search([('channel_id', '=', self.id), ('image_data', '!=', False)], order='id desc', limit=1).image_metadata
#         if last_image_metadata_trimestral and "fatturato totale" in prompt.lower():
#             fatturato_per_annualita = {k: {key: int(val) for key, val in v.items()} for k, v in last_image_metadata_trimestral['fatturato_per_annualita'].items()}  
#             return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata_trimestral['fatturato_per_annualita']}"
#         if last_image_metadata_trimestral and ("massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower()):
#             max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
#             fatturato_max_global = max(max_values)
#             year = last_image_metadata_trimestral['max_fatturato']['year']
#             trimester = last_image_metadata_trimestral['max_fatturato']['trimester']
#             return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

#         if last_image_metadata_trimestral and ("minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower()):
#             min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
#             fatturato_min_global = min(min_values)
#             year = last_image_metadata_trimestral['min_fatturato']['year']
#             trimester = last_image_metadata_trimestral['min_fatturato']['trimester']
#             return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."
        

#         elif "andamento mensile" in prompt.lower():
#             reply, image = andamenti_obj.plot_andamenti_mensili()
#             grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
#             fatturato_per_annualita = {}
            
#             max_fatturato_value = float('-inf')
#             max_fatturato_year = None
#             max_fatturato_month = None

#             min_fatturato_value = float('inf')
#             min_fatturato_year = None
#             min_fatturato_month = None
            
#             for name, group in grouped:
#                 group = group.copy()
#                 group['Mese'] = group['Data fattura'].dt.month
#                 series = group.groupby('Mese')['Totale'].sum()
                
#                 if series.max() > max_fatturato_value:
#                     max_fatturato_value = series.max()
#                     max_fatturato_year = name
#                     max_fatturato_month = series.idxmax()

#                 if series.min() < min_fatturato_value:
#                     min_fatturato_value = series.min()
#                     min_fatturato_year = name
#                     min_fatturato_month = series.idxmin()

#                 fatturato_per_annualita[name] = {
#                     "fatturato_totale": series.sum(),
#                     "fatturato_max": series.max(),
#                     "fatturato_min": series.min()
#                 }

#             metadata = {
#                 "fatturato_per_annualita": fatturato_per_annualita,
#                 "max_fatturato": {
#                     "year": int(max_fatturato_year),
#                     "month": int(max_fatturato_month),
#                     "value": float(max_fatturato_value)
#                 },
#                 "min_fatturato": {
#                     "year": int(min_fatturato_year),
#                     "month": int(min_fatturato_month),
#                     "value": float(min_fatturato_value)
#                 }
#             }

#             # Memorizza l'immagine e i metadati nella chat history
#             output = io.BytesIO()
#             image.save(output, format='PNG')
#             self.env['chat.history'].create({
#                     'channel_id': self.id,
#                     'role': 'assistant',
#                     'content': 'Vedi immagine allegata',
#                     'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
#                     'image_metadata': metadata,
#                     'chart_type': 'monthly'
#                 })

#             mensile_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Monthly Chart'>"
#             return mensile_html
        
#         # last_image_metadata_mensile = self.env['chat.history'].search([('channel_id', '=', self.id), ('image_data', '!=', False)], order='id desc', limit=1).image_metadata
#         last_image_metadata_mensile = self.env['chat.history'].search(
#             [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'monthly')],
#             order='id desc', limit=1).image_metadata
   
#         if last_image_metadata_mensile and (("massimo fatturato" in prompt.lower()) or ("fatturato massimo" in prompt.lower())):
#             max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_mensile['fatturato_per_annualita'].values()]
#             fatturato_max_global = max(max_values)
#             year = last_image_metadata_mensile['max_fatturato']['year']
#             month = last_image_metadata_mensile['max_fatturato']['month']
#             return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {month}° mese dell'anno {year}."

#         if last_image_metadata_mensile and (("minimo fatturato" in prompt.lower()) or ("fatturato minimo" in prompt.lower())):
#             min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_mensile['fatturato_per_annualita'].values()]
#             fatturato_min_global = min(min_values)
#             year = last_image_metadata_mensile['min_fatturato']['year']
#             month = last_image_metadata_mensile['min_fatturato']['month']
#             return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {month}° mese dell'anno {year}."

        
#         # elif "andamento mensile" in prompt.lower():
#         #     reply, image = andamenti_obj.plot_andamenti_mensili()
#         #     output= io.BytesIO()
#         #     image.save(output, format='PNG')
#         #     b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

#         #     img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Monthly Chart'>"

#         #     return img_html
#         elif "previsioni mensili" in prompt.lower():
#             reply, image= previsioni_obj.plot_previsioni_mensili()
#             output= io.BytesIO()
#             image.save(output, format='PNG')
#             b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

#             img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Monthly Forecast'>"

#             return img_html
#         elif "previsioni trimestrali" in prompt.lower():
#             reply, image= previsioni_obj.plot_previsioni_trimestrali()
#             output= io.BytesIO()
#             image.save(output, format='PNG')
#             b64_image = base64.b64encode(output.getvalue()).decode('utf-8')

#             img_html = f"<img src='data:image/png;base64,{b64_image}' alt='Trimestral Forecast'>"

#             return img_html
    
#         else:
#             ICP = self.env['ir.config_parameter'].sudo()
#             openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
#             gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgp_model')
#             gpt_model = 'gpt-3.5-turbo'
#             try:
#                 if gpt_model_id:
#                     gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
#             except Exception as ex:
#                 gpt_model = 'gpt-3.5-turbo'
#                 pass
            
#             user_message = {"role": "user", "content": prompt}
            
#             chat_history.append(user_message)
            
#             total_tokens = sum(len(msg["content"].split()) for msg in chat_history)  # this is a naive token estimate by counting words
            
#             # safety_margin = 500
            
#             max_response_tokens = 1500 - total_tokens
            
#             while max_response_tokens <= 0:
#                 removed_message = chat_history.pop(0)  # remove the oldest message
#                 total_tokens -= len(removed_message["content"].split())  # update total_tokens
#                 max_response_tokens = 1500 - total_tokens
#             try:
#                 chat = openai.ChatCompletion.create(
#                 model=gpt_model,
#                 messages=chat_history,
#                 temperature=0.6,
#                 max_tokens=max_response_tokens,  # the remaining tokens available
#             )
#                 assistant_reply = chat.choices[0].message['content']
                
#                 chat_history.append({"role": "assistant", "content": assistant_reply})
                
#                 return assistant_reply
#             except Exception as e:
#                 print("An error occurred:", e)
#                 raise UserError(_("An error occurred: %s") % e)


    

