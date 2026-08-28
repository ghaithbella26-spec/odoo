import sys
sys.path.insert(0, r'd:\Odoo\odoo')
sys.stdout.reconfigure(encoding='utf-8')

import odoo
from odoo import api, SUPERUSER_ID

odoo.tools.config.parse_config(['-c', r'd:\Odoo\odoo\odoo.conf', '-d', 'dbodoo18'])
registry = odoo.registry('dbodoo18')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Update module list & upgrade modules
    modules_to_upgrade = ['medical_crm_security', 'medical_crm_core', 'crm_adset_integration']
    for mod_name in modules_to_upgrade:
        mod = env['ir.module.module'].search([('name', '=', mod_name)])
        if mod and mod.state == 'installed':
            print(f"Upgrading module: {mod_name}...")
            mod.button_immediate_upgrade()
            print(f"Upgraded {mod_name} successfully.")
    
    cr.commit()

# After module upgrade, re-open registry and env to assign groups
registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Essential Admin Groups
    admin_groups = [
        env.ref('base.group_system'),
        env.ref('base.group_erp_manager'),
        env.ref('medical_crm_security.group_medical_crm_admin'),
        env.ref('sales_team.group_sale_manager'),
        env.ref('crm.group_use_lead'),
        env.ref('sales_team.group_sale_salesman_all_leads'),
    ]
    
    # Get target admin users
    target_logins = ['admin', 'salah@example.com', 'ali@example.com']
    admin_role = env.ref('medical_crm_security.role_medical_crm_admin', raise_if_not_found=False)
    
    for login in target_logins:
        user = env['res.users'].search([('login', '=', login)], limit=1)
        if user:
            print(f"\nGranting full Administrator privileges to user: {user.name} ({user.login})...")
            # Add groups
            for g in admin_groups:
                if g not in user.groups_id:
                    user.write({'groups_id': [(4, g.id)]})
            
            # Assign role if available
            if admin_role:
                user.write({'role_ids': [(4, admin_role.id)]})
            print(f"User {user.name} updated successfully.")
            
    cr.commit()

# Now test rendering settings view and menus for admin and salah
with registry.cursor() as cr:
    for login in ['admin', 'salah@example.com']:
        user = env['res.users'].search([('login', '=', login)], limit=1)
        if not user:
            continue
        u_env = api.Environment(cr, user.id, {})
        print(f"\n================ Testing for {user.name} ({user.login}) ================")
        
        # Test res.config.settings view
        view = u_env['res.config.settings'].get_view(view_type='form')
        import xml.etree.ElementTree as ET
        root = ET.fromstring(view['arch'])
        apps = root.findall('.//app')
        print(f"Visible Settings Apps ({len(apps)}):")
        for app in apps:
            print(f"  * {app.get('string')} (name={app.get('name')}, data-key={app.get('data-key')})")
            
        # Test Menus
        menus = u_env['ir.ui.menu'].load_menus(False)
        print("Configuration menus visible:")
        for root_id in menus['root']['children']:
            m = menus[root_id]
            if 'CRM' in m['name'] or 'مبيعات' in m['name'] or 'Settings' in m['name'] or 'إعدادات' in m['name']:
                print(f"  Root: {m['name']} (id={m['id']})")
                if 'children' in m:
                    for sub_id in m['children']:
                        sub = menus[sub_id]
                        if 'Config' in sub['name'] or 'تهيئة' in sub['name'] or 'Settings' in sub['name'] or 'إعداد' in sub['name']:
                            print(f"    -> {sub['name']} (id={sub['id']})")
                            if 'children' in sub:
                                for sub2_id in sub['children']:
                                    sub2 = menus[sub2_id]
                                    print(f"        -> {sub2['name']} (id={sub2['id']})")
print("\nAll checks completed successfully.")
