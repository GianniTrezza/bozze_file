# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)
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
import logging


_logger = logging.getLogger(__name__)



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
    def _get_last_invoice(self):
        # Recupera tutti i record dalla tabella_fatture
        fatture_records = self.env['tabella_fatture'].search([], order='data DESC', limit=1)  # Supponendo che 'data' sia il campo su cui vuoi ordinare

        # Se esistono record, restituisci il primo (che dovrebbe essere l'ultimo basandosi sull'ordinamento)
        if fatture_records:
            return fatture_records[0]
        else:
            raise UserError("Nessuna fattura trovata.")
    

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
        # if response:
        #     return response
        
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
        
        ICP = self.env['ir.config_parameter'].sudo()
        openai.api_key = ICP.get_param('is_chatgpt_integration.openapi_api_key')
        gpt_model_id = ICP.get_param('is_chatgpt_integration.chatgpt_model')
        gpt_model = 'gpt-4-32k-0613'

        # Estraiamo le fatture se il prompt dell'utente le menziona
        if "fatture" in prompt.lower():
            fatture_records = self.env['tabella.fatture'].search([])
            fatture_data = "\n".join([f"{rec.numero}: {rec.data_fattura}" for rec in fatture_records])
            prompt += f"\n\nDati Fatture:\n{fatture_data}"

        # Qui, possiamo aggiungere ulteriori condizioni basate su ciò che intendiamo per "decodificare".
        # Ad esempio, potremmo avere condizioni che riconoscono determinate parole chiave e modellano la risposta in base a quelle.
        if "quante fatture" in prompt.lower():
            num_fatture = len(fatture_records)
            return f"Ci sono {num_fatture} fatture nella tabella."

        # Potremmo anche riconoscere domande specifiche sulle date o altri dettagli delle fatture
        if "ultima fattura" in prompt:
            last_invoice = self._get_last_invoice()
            return f"L'ultima fattura è la numero {last_invoice.numero} del {last_invoice.data_fattura}."
        # OPPURE: posso anche provare a non utilizzare la funzione get_last_invoice()
        # if "ultima fattura" in prompt.lower():
        #     latest_invoice = fatture_records[-1]
        #     return f"L'ultima fattura è la numero {latest_invoice.numero} del {latest_invoice.data_fattura}."

        # Dopo aver controllato le condizioni specifiche, procediamo con il normale flusso di risposta di gpt-4-32k-0613
        try:
            if gpt_model_id:
                gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
        except Exception:
            gpt_model = 'gpt-4-32k-0613'
            pass

        _logger.info(f"Using model: {gpt_model}")

        try:
            # Modifica qui per utilizzare l'endpoint di chat
            response = openai.ChatCompletion.create(
                model=gpt_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                user=self.env.user.name,
            )
            res = response['choices'][0]['message']['content']
            return res
        except openai.error.OpenAIError as e:
        # Gestione dell'errore qui
            if "maximum context length" in str(e):
                raise UserError(_("The input is too long. Please reduce the size and try again."))
            else:
                raise UserError(_(e))