import shutil
import base64
import os
import sys
import psycopg2

source_logo = r"C:\Users\salah derham\.gemini\antigravity-ide\brain\f8b14e12-9190-49f0-a18d-92dbfd1c03ee\.user_uploaded\media_1787864703366.png"

# 1. Target static directories
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
    logo_bytes = f.read()
    logo_b64 = base64.b64encode(logo_bytes).decode('utf-8')

# 3. Update database res_company logos and partner logos
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

cur.execute("UPDATE res_company SET logo = %s", (logo_bytes,))
cur.execute("""
    UPDATE res_partner 
    SET image_1920 = %s 
    WHERE id IN (SELECT partner_id FROM res_company)
""", (logo_b64,))

# Also update web.base.title or name if relevant
cur.execute("UPDATE res_company SET name = 'مجموعة عيادات بيلاديرم - Belladerm Clinics' WHERE id = 2 OR (parent_id IS NULL AND id != 1)")

conn.commit()
conn.close()
print("Updated res_company and res_partner logo in database.")
