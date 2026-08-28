import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

cur.execute("""
    SELECT c.cron_name, m.model, c.active, c.interval_number, c.interval_type, c.nextcall
    FROM ir_cron c
    JOIN ir_model m ON m.id = c.model_id
    WHERE m.model ILIKE '%crm%' OR c.cron_name ILIKE '%medical%' OR c.cron_name ILIKE '%sla%'
""")
rows = cur.fetchall()
print(f"Total Crons found: {len(rows)}")
for r in rows:
    print(r)

conn.close()
