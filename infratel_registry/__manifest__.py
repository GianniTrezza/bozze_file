# Copyright 2023 Raffaele Amalfitano, Unitiva

{
    'name': 'Infratel Registry',
    'license': 'AGPL-3',
    'author': 'Raffaele Amalfitano, Unitiva',
    'website': 'www.unitiva.it',
    'category': '',
    'version': '1.1.0',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/framework_agreement_views.xml',
        'views/iru_duration_views.xml',
        'views/plant_route_views.xml',
        'views/project_request_views.xml',
        'views/sla_policy_views.xml',
    ],
    'application': False,
    'installable': True
 
}