import sys

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    role_admin = env.ref('medical_crm_security.role_medical_crm_admin', raise_if_not_found=False)
    role_supervisor = env.ref('medical_crm_security.role_medical_crm_supervisor', raise_if_not_found=False)
    role_branch = env.ref('medical_crm_security.role_medical_crm_branch_manager', raise_if_not_found=False)
    role_agent = env.ref('medical_crm_security.role_medical_crm_agent', raise_if_not_found=False)
    role_marketing = env.ref('medical_crm_security.role_medical_crm_marketing', raise_if_not_found=False)

    users = env['res.users'].search([('id', '!=', 1)])
    for u in users:
        login = u.login.lower()
        name = u.name.lower()
        if 'admin' in login or 'admin' in name:
            if role_admin:
                u.write({'role_ids': [(4, role_admin.id)]})
                print(f"Assigned Admin role to {u.name}")
        elif 'super' in login or 'super' in name or 'مشرف' in name:
            if role_supervisor:
                u.write({'role_ids': [(4, role_supervisor.id)]})
                print(f"Assigned Supervisor role to {u.name}")
        elif 'market' in login or 'market' in name or 'تسويق' in name or 'ahmed' in login:
            if role_marketing:
                u.write({'role_ids': [(4, role_marketing.id)]})
                print(f"Assigned Marketing role to {u.name}")
        elif 'mgr' in login or 'manager' in login or 'مدير' in name or 'فرع' in name:
            if role_branch:
                u.write({'role_ids': [(4, role_branch.id)]})
                print(f"Assigned Branch Manager role to {u.name}")
        else:
            if role_agent:
                u.write({'role_ids': [(4, role_agent.id)]})
                print(f"Assigned Agent role to {u.name}")

    cr.commit()
    print("SUCCESS: All users successfully mapped and synchronized to their roles.")
