# Copyright 2023 Raffaele Amalfitano, Unitiva

{
    'name': 'Infratel Account Extension',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano, Unitiva',
    'website': 'www.unitiva.it',
    'category': 'Invoice',
    'version': '1.1.0',
    'depends': [
        'account',
        'infratel_contact_ext',
        'infratel_product_ext'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_views.xml'
    ],
    'application': False,
    'installable': True
}