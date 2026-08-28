import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {'lang': 'ar_001'})
    
    top_menus = env['ir.ui.menu'].search([('parent_id', '=', False)], order='sequence, id')
    print("=== ALL TOP-LEVEL MENUS IN DB ===")
    for m in top_menus:
        print(f"ID: {m.id} | Name: {m.name} | Active: {m.active} | XML ID: {m.get_external_id().get(m.id)}")

