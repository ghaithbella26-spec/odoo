import sys

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Upgrade modules
    modules = env['ir.module.module'].search([('name', 'in', ['medical_crm_core', 'medical_crm_api'])])
    modules.button_immediate_upgrade()
    cr.commit()
    print("SUCCESS: Modules medical_crm_core and medical_crm_api upgraded successfully.")
