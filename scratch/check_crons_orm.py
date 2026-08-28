import sys

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    crons = env['ir.cron'].search([])
    print(f"Total active crons in system: {len(crons)}")
    medical_crons = crons.filtered(lambda c: 'crm' in (c.model_name or '') or 'medical' in (c.name or '').lower())
    for c in medical_crons:
        print(f"Cron: {c.name} | Model: {c.model_name} | Active: {c.active} | Interval: {c.interval_number} {c.interval_type}")
