    # #nuovo tentativo di logica per separare in modo più netto le query legate agli andamenti trimestrali da quelle legate agli andamenti mensili
    # def _get_chatgpt_response(self, prompt, chat_history=[]):
        
    #     andamenti_obj = Andamenti(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
    #     # previsioni_obj = Forecast(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv")
        
    #     # Funzioni helper per separare la logica
    #     def handle_trimestrial(prompt):
    #         if "andamento trimestrale" in prompt.lower():
    #             reply, image = andamenti_obj.plot_andamenti_trimestrali()
    #             grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #             fatturato_per_annualita = {}
    #             max_fatturato_value, min_fatturato_value = float('-inf'), float('inf')
    #             max_fatturato_year, min_fatturato_year, max_fatturato_trimester, min_fatturato_trimester = None, None, None, None
                
    #             for name, group in grouped:
    #                 group['Trimestre'] = group['Data fattura'].dt.quarter
    #                 series = group.groupby('Trimestre')['Totale'].sum()
    #                 if series.max() > max_fatturato_value:
    #                     max_fatturato_value = series.max()
    #                     max_fatturato_year = name
    #                     max_fatturato_trimester = series.idxmax()

    #                 if series.min() < min_fatturato_value:
    #                     min_fatturato_value = series.min()
    #                     min_fatturato_year = name
    #                     min_fatturato_trimester = series.idxmin()

    #                 fatturato_per_annualita[name] = {
    #                     "fatturato_totale": series.sum(),
    #                     "fatturato_max": series.max(),
    #                     "fatturato_min": series.min()
    #                 }

    #             metadata = {
    #                 "fatturato_per_annualita": fatturato_per_annualita,
    #                 "max_fatturato": {
    #                     "year": int(max_fatturato_year),
    #                     "trimester": int(max_fatturato_trimester),
    #                     "value": float(max_fatturato_value)
    #                 },
    #                 "min_fatturato": {
    #                     "year": int(min_fatturato_year),
    #                     "trimester": int(min_fatturato_trimester),
    #                     "value": float(min_fatturato_value)
    #                 }
    #             }

    #             output = io.BytesIO()
    #             image.save(output, format='PNG')
    #             self.env['chat.history'].create({
    #                 'channel_id': self.id,
    #                 'role': 'assistant',
    #                 'content': 'Vedi immagine allegata',
    #                 'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #                 'image_metadata': metadata,
    #                 'chart_type': 'trimestrial'
    #             })

    #             trimestral_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Trimestrial Chart'>"
    #             return trimestral_html
            
    #         last_image_metadata_trimestral = self.env['chat.history'].search(
    #             [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'trimestrial')],
    #             order='id desc', limit=1).image_metadata
            
    #         if "fatturato totale" in prompt.lower():
    #             return f"I fatturati totali per ciascun anno e con relativi picchi trimestrali sono stati i seguenti: {last_image_metadata_trimestral['fatturato_per_annualita']}"

    #         if  "massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower():
    #             max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
    #             fatturato_max_global = max(max_values)
    #             year = last_image_metadata_trimestral['max_fatturato']['year']
    #             trimester = last_image_metadata_trimestral['max_fatturato']['trimester']
    #             return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

    #         if "minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower():
    #             min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_trimestral['fatturato_per_annualita'].values()]
    #             fatturato_min_global = min(min_values)
    #             year = last_image_metadata_trimestral['min_fatturato']['year']
    #             trimester = last_image_metadata_trimestral['min_fatturato']['trimester']
    #             return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {trimester}° trimestre dell'anno {year}."

    #         return None


    #     def handle_monthly(prompt):
    #         if "andamento mensile" in prompt.lower():
    #             reply, image = andamenti_obj.plot_andamenti_mensili()
    #             grouped = andamenti_obj.tabella.groupby(andamenti_obj.tabella['Data fattura'].dt.year)
    #             fatturato_per_annualita = {}
    #             max_fatturato_value, min_fatturato_value = float('-inf'), float('inf')
    #             max_fatturato_year, min_fatturato_year, max_fatturato_month, min_fatturato_month = None, None, None, None
                
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

    #             output = io.BytesIO()
    #             image.save(output, format='PNG')
    #             self.env['chat.history'].create({
    #                 'channel_id': self.id,
    #                 'role': 'assistant',
    #                 'content': 'Vedi immagine allegata',
    #                 'image_data': base64.b64encode(output.getvalue()).decode('utf-8'),
    #                 'image_metadata': metadata,
    #                 'chart_type': 'monthly'
    #             })

    #             monthly_html = f"<img src='data:image/png;base64,{base64.b64encode(output.getvalue()).decode('utf-8')}' alt='Monthly Chart'>"
    #             return monthly_html
            
    #         last_image_metadata_monthly = self.env['chat.history'].search(
    #             [('channel_id', '=', self.id), ('image_data', '!=', False), ('chart_type', '=', 'monthly')],
    #             order='id desc', limit=1).image_metadata
            
    #         if last_image_metadata_monthly and "fatturato totale" in prompt.lower():
    #             return f"I fatturati totali per ciascun anno e con relativi picchi mensili sono stati i seguenti: {last_image_metadata_monthly['fatturato_per_annualita']}"

    #         if last_image_metadata_monthly and ("massimo fatturato" in prompt.lower() or "fatturato massimo" in prompt.lower()):
    #             max_values = [float(year_data['fatturato_max']) for year_data in last_image_metadata_monthly['fatturato_per_annualita'].values()]
    #             fatturato_max_global = max(max_values)
    #             year = last_image_metadata_monthly['max_fatturato']['year']
    #             month = last_image_metadata_monthly['max_fatturato']['month']
    #             return f"Il fatturato massimo del valore di {fatturato_max_global} è stato conseguito nel {month}° mese dell'anno {year}."

    #         if last_image_metadata_monthly and ("minimo fatturato" in prompt.lower() or "fatturato minimo" in prompt.lower()):
    #             min_values = [float(year_data['fatturato_min']) for year_data in last_image_metadata_monthly['fatturato_per_annualita'].values()]
    #             fatturato_min_global = min(min_values)
    #             year = last_image_metadata_monthly['min_fatturato']['year']
    #             month = last_image_metadata_monthly['min_fatturato']['month']
    #             return f"Il fatturato minimo del valore di {fatturato_min_global} è stato conseguito nel {month}° mese dell'anno {year}."

    #         return None
    #     # Chiamate principali
    #     response = handle_trimestrial(prompt)
    #     if response:
    #         return response
        
    #     response = handle_monthly(prompt)
    #     if response:
    #         return response

    #     # return "Non ho potuto elaborare la tua richiesta."
    #     else:
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

# def handle_trimestrial_graphic(prompt):
#             year = None
#             if "andamento trimestrale" in prompt.lower():
#                 year = get_year_from_prompt(prompt)
#             if year:
#                 reply, image = andamenti_obj.plot_andamenti_trimestrali_per_anno(year)
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


#INDICE DI AFFIDABILITà
# elif choice== "Indice di affidabilità":
#             import pandas as pd
#             import numpy as np
#             import matplotlib.pyplot as plt
#             from statsmodels.tsa.statespace.sarimax import SARIMAX
            
#             tabella = load_iris()
#             tabella = pd.read_csv(r"C:\Users\giova\OneDrive\Desktop\tabella_fatture.csv", header=None,
#                                   names=["Cliente", "Data fattura", "Numero", "Addetto vendite", "Data scadenza",
#                                          "Documento origine", "Insoluta", "Imponibile", "Imposta", "Totale",
#                                          "Importo dovuto", "Stato e-fattura"])
#             print(tabella["Cliente"])
#             counting_clienti=tabella["Cliente"].nunique()
#             print("Il numero dei clienti è", counting_clienti)

            
#             # stato_fatture_cliente = tabella.groupby("Cliente")["Stato"].value_counts()
#             stato_fatture_cliente = tabella.groupby("Cliente")["Stato e-fattura"].value_counts().unstack(fill_value=0)
#             solo_aperte= stato_fatture_cliente[" Aperta"]
#             print("Lo stato delle fatture è\n\n", solo_aperte)
#             totale_fatture_cliente = stato_fatture_cliente.sum(axis=1).sort_values(ascending=False).head(counting_clienti)
#             fatture_pagate_cliente = stato_fatture_cliente[" Pagata"].nlargest(counting_clienti)
#             fatture_aperte_cliente = stato_fatture_cliente[" Pagata"].nsmallest(counting_clienti)
#             solvibilità_cliente= (fatture_pagate_cliente/totale_fatture_cliente)*100
#             insolvibilità_cliente= (fatture_aperte_cliente/totale_fatture_cliente)*100


#             print("L'insolvibilità dei clienti è", insolvibilità_cliente)
#             print("La solvibilità dei clienti è", solvibilità_cliente)
#             print("il numero di fatture aperte è", fatture_aperte_cliente)
#             print("Il numero di fatture totali è", totale_fatture_cliente)

#             from textwrap import wrap

#             plt.figure(figsize=(12, 10))
#             solvibilità_cliente.plot(kind="bar", color="red")
#             plt.title("Fatture Pagate/Fatture totali per cliente")
#             plt.xlabel("Cliente")
#             plt.ylabel("Ratio (%)")
#             fatture_labels_1 = [ '\n'.join(wrap(label, 15)) for label in solvibilità_cliente.index]
#             plt.xticks(range(len(fatture_labels_1)), fatture_labels_1, rotation=45, ha='right', fontsize=10)  # Rotazione a 45 gradi, allineamento a destra
            
#             # migliori_10_clienti_solvibilità= solvibilità_cliente.nlargest(10)
#             #oppure
#             peggiori_10_clienti_solvibilità = solvibilità_cliente.nsmallest(10)
            
#             #1 PLOT PER I MIGLIORI CLIENTI
#             # plt.figure(figsize=(12, 10))
#             # migliori_10_clienti_solvibilità.plot(kind="bar", color="red")
#             # plt.title("Fatture Pagate/Fatture totali per cliente")
#             # plt.xlabel("Cliente")
#             # plt.ylabel("Ratio(%)")
#             # fatture_labels_migliori = [ '\n'.join(wrap(label, 15)) for label in migliori_10_clienti_solvibilità.index]
#             # plt.xticks(range(len(fatture_labels_migliori)), fatture_labels_migliori, rotation=45, ha='right', fontsize=10)

#             #2 PLOT PER I PEGGIORI CLIENTI
#             plt.figure(figsize=(12,10))
#             peggiori_10_clienti_solvibilità.plot(kind="bar", color="pink")
#             plt.title("Fatture Pagate/Fatture totali per i peggiori clienti")
#             plt.xlabel("Cliente")
#             plt.ylabel("Ratio(%)")
#             fatture_labels_peggiori= [ '\n'.join(wrap(label, 15)) for label in peggiori_10_clienti_solvibilità.index]
#             plt.xticks(range(len(fatture_labels_peggiori)), fatture_labels_peggiori, rotation=45, ha='right', fontsize=10)


            
#             # Converti il grafico in un'immagine
#             buffer = io.BytesIO()
#             plt.savefig(buffer, format='png')
#             buffer.seek(0)
#             image_data = buffer.getvalue()
#             image_fatture_clienti = Image.open(io.BytesIO(image_data))

#             reply_fatture_clienti = "Ecco l'analisi delle fatture per i clienti di Unitiva"
#             return reply_fatture_clienti, image_fatture_clienti


# -*- coding: utf-8 -*-
from odoo import api, fields, models

# Il sistema deve essere predisposto per gestire il processo di accreditamento di strutture
# sanitarie.
# Per accreditare una struttura, è necessario registrare all’interno del sistema una pratica,
# all’interno della quale devono essere riportate le seguenti informazioni:
# ● Codice pratica: ACCR/ANNO/YYY, con ANNO = anno di registrazione della pratica
# all’interno del sistema (es. 2023), ed YYY = sequenza incrementale di 3 cifre, del tipo
# 001, 002;
# ● Autore registrazione: fare riferimento alla struttura dati res.users già presente a
# sistema. La voce deve essere automaticamente compilata con l’utente che sta
# registrando la pratica e non può essere modificata.
# ● Tipologia pratica: struttura dati/anagrafica a se stante, riutilizzabile in altre pratiche,
# costituita dalla sola voce testuale “Nome”. Dato obbligatorio.
# ● Richiedente: fare riferimento alla struttura dati res.partner già presente a sistema. Il
# richiedente deve essere un contatto di tipo persona.
# ● Struttura da accreditare: fare riferimento alla struttura dati res.partner già presente a
# sistema. La struttura sanitaria deve essere un contatto di tipo azienda,
# opportunamente contrassegnato come “È una struttura sanitaria”. Dato obbligatorio.
# ● Descrizione: blocco descrittivo in formato html, per aggiungere informazioni
# aggiuntive alla pratica.

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description= "Patient records"

    codice_pratica=fields.Char(string= "codice_pratica")

    name= fields.Char(string= "Name", required= True)
    age= fields.Integer(string= "Age")
    is_child= fields.Boolean(string="Is child?")
    notes= fields.Text(string= "Notes")
    gender=fields.Selection([("male", "Male"), ("female", "Female"), ("others", "Others")])