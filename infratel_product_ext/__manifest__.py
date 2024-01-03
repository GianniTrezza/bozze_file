# Copyright 2023 Raffaele Amalfitano, Unitiva

{
    'name': 'Infratel Product Extension',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano, Unitiva',
    'website': 'www.unitiva.it',
    'category': 'Sales',
    'version': '1.0.1',
    'depends': [
        'infratel_registry',
        'product',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/framework_agreement_views.xml',
        'views/product_template_views.xml',
    ],
    'application': False,
    'installable': True
}