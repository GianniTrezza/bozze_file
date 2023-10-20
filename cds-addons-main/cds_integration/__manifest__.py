# Copyright 2023 Raffaele Amalfitano

{
    'name': 'CDS Integration',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano',
    'website': 'www.unitiva.it',
    'category': '',
    'version': '1.2.0',
    'depends': [
        'auth_jwt',
        'contacts',
        'crm',
        'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/auth_jwt_validator.xml',
        'views/additional_data_structure_views.xml',
        'views/crm_lead_views.xml',
        'views/product_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml'
    ],
    'application': False,
    'installable': True
}