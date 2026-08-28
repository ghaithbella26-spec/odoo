import sys
sys.path.insert(0, r'd:\Odoo\odoo')
sys.stdout.reconfigure(encoding='utf-8')

import odoo
from odoo import api, SUPERUSER_ID
import xml.etree.ElementTree as ET

odoo.tools.config.parse_config(['-c', r'd:\Odoo\odoo\odoo.conf', '-d', 'dbodoo18'])
registry = odoo.registry('dbodoo18')

with registry.cursor() as cr:
    for login in ['admin', 'salah@example.com', 'ali@example.com']:
        env = api.Environment(cr, SUPERUSER_ID, {})
        user = env['res.users'].search([('login', '=', login)], limit=1)
        if not user:
            continue
        u_env = api.Environment(cr, user.id, {})
        print(f"\n=======================================================")
        print(f"User: {user.name} (login: {user.login}, id: {user.id})")
        print(f"  - group_system (الإعدادات): {u_env.user.has_group('base.group_system')}")
        print(f"  - group_erp_manager (صلاحيات الوصول): {u_env.user.has_group('base.group_erp_manager')}")
        print(f"  - group_medical_crm_admin (مدير CRM الطبي): {u_env.user.has_group('medical_crm_security.group_medical_crm_admin')}")
        print(f"  - group_sale_manager (مدير المبيعات/CRM): {u_env.user.has_group('sales_team.group_sale_manager')}")
        
        # Test res.config.settings form view
        view = u_env['res.config.settings'].get_view(view_type='form')
        root = ET.fromstring(view['arch'])
        apps = root.findall('.//app')
        print(f"\nVisible Settings Apps in General Settings ({len(apps)}):")
        for app in apps:
            app_name = app.get('name')
            app_string = app.get('string')
            app_key = app.get('data-key') or app.get('name')
            blocks = app.findall('.//block')
            print(f"  ▶ [{app_string}] (key={app_key}, name={app_name}, blocks={len(blocks)})")
            for b in blocks:
                b_title = b.get('title') or b.get('string') or 'General'
                settings = b.findall('.//setting')
                print(f"     - Block: '{b_title}' ({len(settings)} settings)")
                
        # Test Top Menus
        menus = u_env['ir.ui.menu'].load_menus(False)
        print("\nConfiguration Menus Visible in Top Bar:")
        for root_id in menus['root']['children']:
            m = menus[root_id]
            if m['id'] in [423, 394, 1]: # Medical CRM, CRM, Settings
                print(f"  App: {m['name']} (id={m['id']})")
                if 'children' in m:
                    for sub_id in m['children']:
                        sub = menus[sub_id]
                        if 'Config' in sub['name'] or 'تهيئة' in sub['name'] or 'Settings' in sub['name'] or 'إعداد' in sub['name']:
                            print(f"    └─ Menu: {sub['name']} (id={sub['id']})")
                            if 'children' in sub:
                                for sub2_id in sub['children']:
                                    sub2 = menus[sub2_id]
                                    print(f"        ├── Subitem: {sub2['name']} (id={sub2['id']})")
