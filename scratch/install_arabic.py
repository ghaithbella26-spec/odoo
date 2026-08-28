import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Activate Arabic Language (ar_001)
    lang = env['res.lang'].search([('code', '=', 'ar_001')], limit=1)
    if not lang:
        lang = env['res.lang'].search([('code', '=', 'ar_SY')], limit=1)
    
    if lang:
        lang.write({'active': True})
        print(f"Activated language: {lang.name} ({lang.code})")
        
        # Load / Install translation terms for ar_001 across all installed modules
        try:
            wizard = env['base.language.install'].create({
                'lang_ids': [(4, lang.id)],
                'overwrite': True,
            })
            wizard.lang_install()
            print(f"Installed and loaded translations for {lang.code}")
        except Exception as e:
            print("Wizard install exception (if any):", e)
            
        # 2. Set Arabic as default language for admin and main users
        admin_user = env['res.users'].search([('login', '=', 'admin')], limit=1)
        if admin_user:
            admin_user.write({'lang': lang.code})
            print(f"Updated user '{admin_user.name}' language to {lang.code}")
            
        # Also update all active internal users
        internal_users = env['res.users'].search([('share', '=', False)])
        for u in internal_users:
            u.write({'lang': lang.code})
            print(f"Updated user '{u.name}' ({u.login}) language to {lang.code}")

    cr.commit()
    print("SUCCESS: Arabic language enabled and set for users.")
