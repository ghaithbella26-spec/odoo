# -*- coding: utf-8 -*-
{
    'name': 'Medical CRM - AdSet Integration',
    'version': '18.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Link Ad Sets with Medical CRM Leads and receive leads via direct Webhooks API',
    'description': """
        This module allows managing Ad Sets directly inside Medical CRM and provides a Webhook endpoint
        to automatically receive and assign incoming leads from advertising platforms (Meta, Google, TikTok).
    """,
    'author': 'Medical CRM',
    'depends': ['crm', 'utm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_adset_views.xml',
        'views/crm_lead_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
