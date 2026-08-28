import sys
import base64
import os
import shutil

source_logo = r"C:\Users\salah derham\.gemini\antigravity-ide\brain\f8b14e12-9190-49f0-a18d-92dbfd1c03ee\.user_uploaded\media_1787864703366.png"

# 1. Copy to static image assets
dest_dir1 = r"d:\Odoo\odoo\projects\myaddons\medical_crm_dashboard\static\src\img"
dest_dir2 = r"d:\Odoo\odoo\projects\myaddons\medical_crm_core\static\src\img"

os.makedirs(dest_dir1, exist_ok=True)
os.makedirs(dest_dir2, exist_ok=True)

dest_logo1 = os.path.join(dest_dir1, "belladerm_logo.png")
dest_logo2 = os.path.join(dest_dir2, "belladerm_logo.png")

shutil.copyfile(source_logo, dest_logo1)
shutil.copyfile(source_logo, dest_logo2)
print("Copied logo to static directories.")

# 2. Read logo as Base64
with open(source_logo, "rb") as f:
    logo_b64 = base64.b64encode(f.read())

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env['res.company'].search([])
    for comp in companies:
        comp.write({
            'logo': logo_b64,
        })
        if comp.partner_id:
            comp.partner_id.write({'image_1920': logo_b64})
        print(f"Set Belladerm logo on company: {comp.name} (ID: {comp.id})")

    cr.commit()
    print("SUCCESS: Belladerm logo applied to all companies in Odoo.")
