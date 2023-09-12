{
    'name': 'new_accreditamento',
    'author': 'Giovanni Trezza',
    'category': 'Health',
    'depends': ['base', 'mail'],
    'website': 'www.odoo_accreditamento.tech',
    'summary': 'Processo accreditamento (Strutture Sanitarie)', 
    'data': [
        'security/ir.model.access.csv',
        'security/sicurezza.xml',
        'views/accreditation.xml',
        'views/struttura_sanitaria.xml',
        'views/tipologia_pratica.xml',
        'views/menu.xml'      
    ],  
    'installable': True,
    'application': True,
}
