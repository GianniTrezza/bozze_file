{
    'name': 'Prenoto Stanze',
    'author': 'Giovanni Trezza',
    'category': 'Booking',
    'depends': ['base', 'account', 'sale'],
    'website': 'www.odoo_prenoto_stanze.tech',
    'summary': 'Prenoto Stanze: Integrazione con Octorate', 
    'data': [
        'views/info_booking.xml',
        'security/security.xml'   
    ],  
    'installable': True,
    'application': True,
}