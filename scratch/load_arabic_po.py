import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    lang = env['res.lang'].search([('code', '=', 'ar_001')], limit=1)
    if lang:
        lang.write({'active': True})
        print(f"Active Arabic Language: {lang.name} ({lang.code})")
        
        mods = env['ir.module.module'].search([('state', '=', 'installed')])
        print(f"Updating translations for {len(mods)} installed modules...")
        mods._update_translations([lang.code], overwrite=True)
        print("Translations loaded successfully!")
        
        # Set Arabic for all active users
        users = env['res.users'].search([('active', '=', True)])
        users.write({'lang': lang.code})
        print(f"Set Arabic (ar_001) for {len(users)} users.")

    cr.commit()
    print("FINISHED: Arabic installation and translation complete.")
