import psycopg2
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'ir_ui_menu' AND column_name = 'name'")
print('ir_ui_menu.name column type:', cur.fetchall())

cur.execute("SELECT id, name FROM ir_ui_menu WHERE name IS NOT NULL LIMIT 10")
for r in cur.fetchall():
    print(r)

print("\n--- Medical Menus in DB ---")
cur.execute("SELECT id, name FROM ir_ui_menu WHERE name::text ILIKE '%medical%' OR name::text ILIKE '%pipeline%' OR name::text ILIKE '%clinic%' OR name::text ILIKE '%lead%'")
for r in cur.fetchall():
    print(r)

conn.close()
