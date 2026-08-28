import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

cur.execute("""
    SELECT a.id, a.name->>'ar_001', a.name->>'en_US', a.res_model, d.module, d.name 
    FROM ir_act_window a
    LEFT JOIN ir_model_data d ON d.model = 'ir.actions.act_window' AND d.res_id = a.id
    WHERE a.res_model = 'res.config.settings' OR a.name::text ILIKE '%General Settings%' OR a.name::text ILIKE '%الإعدادات%'
""")
for r in cur.fetchall():
    print(r)

conn.close()
