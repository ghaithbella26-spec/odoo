import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# The 3 allowed Top-level Apps:
# 1. Medical CRM (id: 423 / xmlid: medical_crm_core.medical_crm_menu_root)
# 2. CRM (id: 394 / xmlid: crm.crm_menu_root)
# 3. Settings (id: 1 / xmlid: base.menu_administration)

allowed_menu_ids = [423, 394, 1]

# 1. Ensure the 3 target menus are active
cur.execute("UPDATE ir_ui_menu SET active = true WHERE id IN %s", (tuple(allowed_menu_ids),))

# 2. Deactivate all other top-level menus (parent_id IS NULL)
cur.execute("""
    UPDATE ir_ui_menu 
    SET active = false 
    WHERE parent_id IS NULL 
      AND id NOT IN %s
""", (tuple(allowed_menu_ids),))

conn.commit()

# Verify active top-level menus
cur.execute("""
    SELECT id, name->>'ar_001', name->>'en_US', active 
    FROM ir_ui_menu 
    WHERE parent_id IS NULL AND active = true 
    ORDER BY sequence, id
""")
print("=== ACTIVE TOP-LEVEL APPS NOW ===")
for r in cur.fetchall():
    print(f"ID: {r[0]} | Arabic: {r[1]} | English: {r[2]} | Active: {r[3]}")

conn.close()
