{
    'name': 'new_accreditamento',
    'author': 'Giovanni Trezza',
    'category': 'Health',
    'depends': ['base', 'mail'],
    'website': 'www.odoo_accreditamento.tech',
    'summary': 'Processo accreditamento (Strutture Sanitarie)', 
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'security/user.xml',
        'security/manager.xml',
        'views/accreditation.xml',
        'views/struttura_sanitaria.xml',
        'views/tipologia_pratica.xml',
        'views/hospital_accreditation_report.xml',
        'views/menu.xml'      
    ],  
    'installable': True,
    'application': True,
}
