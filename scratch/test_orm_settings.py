import sys
sys.path.insert(0, r'd:\Odoo\odoo')
sys.stdout.reconfigure(encoding='utf-8')

import odoo
from odoo import api, SUPERUSER_ID

odoo.tools.config.parse_config(['-c', r'd:\Odoo\odoo\odoo.conf', '-d', 'dbodoo18'])
registry = odoo.registry('dbodoo18')

with registry.cursor() as cr:
    env = api.Environment(cr, 2, {}) # Mitchell Admin uid=2
    user = env.user
    print(f"Logged in as: {user.name} ({user.login})")
    
    # Check if user has groups:
    print("Has group base.group_system:", user.has_group('base.group_system'))
    print("Has group sales_team.group_sale_manager:", user.has_group('sales_team.group_sale_manager'))
    print("Has group medical_crm_security.group_medical_crm_admin:", user.has_group('medical_crm_security.group_medical_crm_admin'))

    # Load res.config.settings view definition for admin
    settings_model = env['res.config.settings']
    view = settings_model.get_view(view_type='form')
    arch = view['arch']
    
    # Check what apps are present in the arch
    import xml.etree.ElementTree as ET
    root = ET.fromstring(arch)
    apps = root.findall('.//app')
    print(f"\nFound {len(apps)} <app> elements in res.config.settings for Admin:")
    for app in apps:
        print(f" - string: {app.get('string')}, name: {app.get('name')}, data-string: {app.get('data-string')}, notApp: {app.get('notApp')}")

    # Check menus visible for admin
    menus = env['ir.ui.menu'].load_menus(False)
    print("\nRoot menus visible in webclient:")
    for child_id in menus['root']['children']:
        m = menus[child_id]
        print(f"Root Menu: {m['name']} (id={m['id']}, xmlid={m['xmlid']})")
        if 'children' in m:
            for sub_id in m['children']:
                sub = menus[sub_id]
                print(f"   -> Submenu: {sub['name']} (id={sub['id']}, xmlid={sub['xmlid']})")
                if 'children' in sub:
                    for sub2_id in sub['children']:
                        sub2 = menus[sub2_id]
                        print(f"       -> Sub-sub: {sub2['name']} (id={sub2['id']}, xmlid={sub2['xmlid']})")
