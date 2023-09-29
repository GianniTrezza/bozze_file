{
    'name': 'Prenotazione stanza',
    'version': '1.0',
    'author': 'Simone',
    'description': 'Prenotazione stanze: integrazione con Octorate ',
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/booking_info.xml',
        'views/menu.xml',
    ],
    'application': True

}