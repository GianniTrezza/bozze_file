{
    'name': 'Status Bar e nuovi pulsanti - Sale',
    'version': '1.0',
    'description': 'Estensione dei bottoni e dello statusbar nel modulo di Vendite ',
    'category': 'Sales',
    'author': 'Gianni Trezza',
    'depends': ['sale', 'infratel_sale_ext'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/status_bar_sale.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
