import sys

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    roles = env['res.users.role'].search([])
    for r in roles:
        print(f"Role ID: {r.id}, Code: {r.code}, Name: {r.name}")

    role_map = {r.code: r for r in roles}

    users = env['res.users'].search([('id', '!=', 1)])
    for u in users:
        login = (u.login or '').lower()
        name = (u.name or '').lower()
        matched_role = None
        if 'admin' in login or 'admin' in name:
            matched_role = role_map.get('admin')
        elif 'super' in login or 'super' in name or 'مشرف' in name:
            matched_role = role_map.get('supervisor')
        elif 'market' in login or 'market' in name or 'تسويق' in name or 'ahmed' in login:
            matched_role = role_map.get('marketing') or role_map.get('marketing_manager')
        elif 'mgr' in login or 'manager' in login or 'مدير' in name or 'فرع' in name:
            matched_role = role_map.get('branch_manager') or role_map.get('branch_mgr')
        else:
            matched_role = role_map.get('agent') or role_map.get('call_center_agent')

        if matched_role:
            u.write({'role_ids': [(6, 0, [matched_role.id])]})
            print(f"Assigned {u.name} ({u.login}) -> Role: {matched_role.name}")

    cr.commit()
    print(f"SUCCESS: {len(users)} users mapped to roles!")
