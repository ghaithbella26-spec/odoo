import psycopg2
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# 1. Update Main Parent Company Name
cur.execute("""
    UPDATE res_company 
    SET name = 'مجموعة عيادات الجلد الذهبي - Golden Skin Clinics' 
    WHERE id = 2 OR (parent_id IS NULL AND id != 1)
""")
print("Updated Main Company name.")

# 2. Update Web Title parameter
cur.execute("""
    INSERT INTO ir_config_parameter (key, value)
    VALUES ('web.base.title', 'الجلد الذهبي - Golden Skin CRM')
    ON CONFLICT (key) DO UPDATE SET value = 'الجلد الذهبي - Golden Skin CRM'
""")
print("Updated web.base.title.")

# 3. Update Medical CRM App Menu Name
cur.execute("""
    UPDATE ir_ui_menu 
    SET name = %s 
    WHERE id = 423
""", (json.dumps({'en_US': 'Golden Skin CRM', 'ar_001': 'الجلد الذهبي - Golden Skin CRM'}),))
print("Updated Medical CRM Menu name.")

# 4. Update Launcher Action Name
cur.execute("""
    UPDATE ir_act_window 
    SET name = %s 
    WHERE id = 682
""", (json.dumps({'en_US': 'Golden Skin CRM', 'ar_001': 'الرئيسية - الجلد الذهبي Golden Skin CRM'}),))

conn.commit()
conn.close()
print("SUCCESS: Database updated to 'الجلد الذهبي - Golden Skin CRM'.")
