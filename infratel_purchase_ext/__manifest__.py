# Copyright 2023 Raffaele Amalfitano, Unitiva

{
    'name': 'Infratel Purchase Extension',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano, Unitiva',
    'website': 'www.unitiva.it',
    'category': 'Purchases',
    'version': '1.1.0',
    'depends': [
        'infratel_contact_ext',
        'purchase'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/menu_views.xml'
    ],
    'application': False,
    'installable': True
}