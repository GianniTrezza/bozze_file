{
    'name': 'Prenotazione stanze e appartamenti',
    'version': '1.0',
    'author': 'Gianni',
    'description': 'Prenotazione stanze: integrazione con Octorate ',
    'depends': ['base', 'utm', 'account', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/booking_info.xml',
    ],
    'application': True

}