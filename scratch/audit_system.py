import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {'lang': 'ar_001'})
    
    print("=== 1. AUDITING MENUS ===")
    menus = env['ir.ui.menu'].search([('name', '!=', False)])
    medical_menus = [m for m in menus if 'medical' in (m.complete_name or '').lower() or 'crm' in (m.complete_name or '').lower()]
    for m in medical_menus[:15]:
        print(f"Menu ID: {m.id} | Name: {m.name} | Complete: {m.complete_name}")

    print("\n=== 2. AUDITING STAGES ===")
    stages = env['crm.stage'].search([])
    for s in stages:
        print(f"Stage ID: {s.id} | Name: {s.name} | SLA: {s.sla_hours}h | Seq: {s.sequence}")

    print("\n=== 3. AUDITING ACTIVITY TYPES ===")
    acts = env['mail.activity.type'].search([])
    for a in acts:
        print(f"Activity: {a.name} | Category: {a.category} | Delay: {a.delay_count} {a.delay_unit}")

    print("\n=== 4. AUDITING DEPARTMENTS & SERVICES ===")
    clinics = env['medical.clinic'].search([])
    for c in clinics:
        print(f"Dept: {c.name} ({c.code}) -> Services count: {len(c.service_ids)}")
        for s in c.service_ids[:2]:
            print(f"   * {s.name} ({s.price} SAR)")

    print("\n=== 5. AUDITING USER ROLES ===")
    roles = env['res.users.role'].search([])
    for r in roles:
        print(f"Role: {r.name} ({r.code}) -> Users: {len(r.user_ids)} | Groups: {len(r.group_ids)}")

