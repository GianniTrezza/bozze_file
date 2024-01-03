# Copyright 2023 Raffaele Amalfitano, Unitiva

{
    'name': 'Infratel Sale Extension',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano, Unitiva',
    'website': 'www.unitiva.it',
    'category': 'Sales',
    'version': '1.1.0',
    'depends': [
        'infratel_contact_ext',
        'infratel_registry',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/menu_views.xml'
    ],
    'application': False,
    'installable': True
}