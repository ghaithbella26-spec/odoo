import sys
sys.path.insert(0, r'd:\Odoo\odoo')
sys.stdout.reconfigure(encoding='utf-8')

import odoo
from odoo import api

odoo.tools.config.parse_config(['-c', r'd:\Odoo\odoo\odoo.conf', '-d', 'dbodoo18'])
registry = odoo.registry('dbodoo18')

with registry.cursor() as cr:
    env = api.Environment(cr, odoo.SUPERUSER_ID, {})
    for login in ['admin', 'salah@example.com', 'ali@example.com']:
        user = env['res.users'].search([('login', '=', login)])
        if user:
            print(f"\n--- User {user.name} ({user.login}, id={user.id}) ---")
            print("Groups:", [g.full_name for g in user.groups_id])
