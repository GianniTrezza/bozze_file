{
    'name': 'Prenotazione stanze e appartamenti',
    'version': '1.0',
    'author': 'Gianni',
    'description': 'Prenotazione stanze: integrazione con Octorate ',
    'depends': ['base', 'utm', 'account', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/booking_info.xml',
        'views/menu.xml',
    ],
    'application': True

}