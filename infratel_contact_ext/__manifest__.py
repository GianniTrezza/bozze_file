# Copyright 2023 Raffaele Amalfitano, Unitiva

{
    'name': 'Infratel Contact Extension',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano, Unitiva',
    'website': 'www.unitiva.it',
    'category': 'CRM',
    'version': '1.1.0',
    'depends': [
        'contacts',
        'infratel_registry'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/framework_agreement_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml',
    ],
    'application': False,
    'installable': True
}