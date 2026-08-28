import sys
sys.path.insert(0, r'd:\Odoo\odoo')
sys.stdout.reconfigure(encoding='utf-8')

import odoo
from odoo import api

odoo.tools.config.parse_config(['-c', r'd:\Odoo\odoo\odoo.conf', '-d', 'dbodoo18'])
registry = odoo.registry('dbodoo18')

with registry.cursor() as cr:
    env = api.Environment(cr, odoo.SUPERUSER_ID, {})
    users = env['res.users'].search([])
    print("=== All Users and their CRM / Admin status ===")
    for u in users:
        u_env = api.Environment(cr, u.id, {})
        has_system = u_env.user.has_group('base.group_system')
        has_erp = u_env.user.has_group('base.group_erp_manager')
        has_sale_manager = u_env.user.has_group('sales_team.group_sale_manager')
        has_med_admin = u_env.user.has_group('medical_crm_security.group_medical_crm_admin')
        has_med_readonly = u_env.user.has_group('medical_crm_security.group_medical_crm_readonly')
        print(f"User: id={u.id}, login={u.login}, name={u.name}")
        print(f"   group_system: {has_system}, sale_manager: {has_sale_manager}, med_admin: {has_med_admin}, erp_manager: {has_erp}")
