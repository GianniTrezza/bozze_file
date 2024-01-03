# Copyright 2023 Raffaele Amalfitano, Unitiva

{
    'name': 'Infratel CRM Extension',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano, Unitiva',
    'website': 'www.unitiva.it',
    'category': 'CRM',
    'version': '1.1.0',
    'depends': [
        'crm',
        'infratel_contact_ext',
        'infratel_product_ext'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_views.xml',
        'views/menu_views.xml'
    ],
    'application': False,
    'installable': True
}