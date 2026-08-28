import psycopg2
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# 1. Inspect all JSONB columns in tables that hold user-facing names
cur.execute("""
    SELECT table_name, column_name 
    FROM information_schema.columns 
    WHERE data_type = 'jsonb' 
      AND table_schema = 'public'
      AND table_name IN ('ir_ui_menu', 'ir_act_window', 'crm_stage', 'crm_lost_reason', 'mail_activity_type', 'medical_clinic', 'medical_service', 'res_groups', 'res_users_role')
""")
for r in cur.fetchall():
    print(r)

conn.close()
