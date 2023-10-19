{
    'name': 'Prenota con Noi!',
    'version': '16.0.1.0',
    'author': 'Gianni',
    'description': 'Prenotazione stanze: integrazione con Octorate ',
    'depends': ['base', 'account', 'web'],
    'data': [
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',  
        'views/stampa_prenotazione.xml', 
        'views/prenotazione_info.xml',
    ],

    'application': True

}