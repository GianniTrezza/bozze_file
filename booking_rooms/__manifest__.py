{
    'name': 'Prenotazione Stanze',
    'author': 'Giovanni Trezza',
    'category': 'Sales',
    'depends': ['base', 'mail'],
    'website': 'www.odoo_prenotazione_stanze.tech',
    'summary': 'Prenoazione Stanze: Integrazione con Octorate', 
    'data': [
        'data/ir_sequence.xml',
        'views/info_book.xml',
        'security/security.xml'   
    ],  
    'installable': True,
    'application': True,
}