{
    'name': 'Infratel Joining Sale Purchase',
    'version': '1.0',
    'description': 'Modulo per creare automaticamente un ordine di acquisto a partire da un ordine di vendita',
    'category': 'Sales',
    'author': 'Gianni Trezza',
    'depends': ['sale', 'purchase', 'infratel_sale_ext', 'infratel_purchase_ext'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_purchase_views.xml',
        'views/smart_button_sale_purchase.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
