import sys

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    teams = env['crm.team'].search([])
    print(f"Total Sales Teams found: {len(teams)}")
    
    for team in teams:
        old_comp = team.company_id.name if team.company_id else 'None (Shared)'
        team.write({'company_id': False})
        print(f"Updated Team '{team.name}' (ID: {team.id}): Company was '{old_comp}' -> now 'Shared (All Branches)'")

    # Set multi-company access on all active users
    parent_comp = env['res.company'].search([('parent_id', '=', False), ('id', '!=', 1)], limit=1)
    all_branches = env['res.company'].search([])
    
    users = env['res.users'].search([('id', '!=', 1)])
    for u in users:
        u.write({
            'company_ids': [(6, 0, all_branches.ids)],
            'company_id': parent_comp.id if parent_comp else u.company_id.id
        })
        print(f"Set all branch companies access on user: {u.name}")

    cr.commit()
    print("SUCCESS: All Call Center & Sales Teams are now shared globally across all branches, and users have full multi-branch access.")
