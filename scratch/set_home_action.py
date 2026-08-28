import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18', '-u', 'medical_crm_core,medical_crm_dashboard'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Locate the Medical Home Launcher action
    action = env.ref('medical_crm_dashboard.action_medical_home_launcher', raise_if_not_found=False)
    if not action:
        action = env['ir.actions.client'].search([('tag', '=', 'medical_home_launcher')], limit=1)
        
    if action:
        print(f"Found Medical Home Launcher Action: ID {action.id} - {action.name}")
        
        # 2. Set Home Action on res.users (admin and all users)
        users = env['res.users'].search([('active', '=', True)])
        users.write({'action_id': action.id})
        print(f"Updated Home Action for {len(users)} users.")
        
        # 3. Set Home Menu sequence
        home_menu = env.ref('medical_crm_dashboard.menu_medical_home_launcher_root', raise_if_not_found=False)
        if home_menu:
            home_menu.write({'sequence': 0, 'active': True})
            print(f"Home Menu sequence set to 0 (ID: {home_menu.id})")

    cr.commit()
    print("SUCCESS: Medical Home Launcher is now the default Home Action.")
