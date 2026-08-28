import sys
sys.path.insert(0, r'd:\Odoo\odoo')
sys.stdout.reconfigure(encoding='utf-8')

import odoo
from odoo import api, SUPERUSER_ID

odoo.tools.config.parse_config(['-c', r'd:\Odoo\odoo\odoo.conf', '-d', 'dbodoo18'])
registry = odoo.registry('dbodoo18')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    mod = env['ir.module.module'].search([('name', '=', 'medical_crm_dashboard')])
    if mod and mod.state == 'installed':
        print("Upgrading medical_crm_dashboard to refresh asset bundles...")
        mod.button_immediate_upgrade()
        print("medical_crm_dashboard upgraded successfully.")
    cr.commit()
