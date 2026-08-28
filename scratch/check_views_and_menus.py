import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# Check groups assigned to menus 406, 407, 430, 434
cur.execute('''
    SELECT rel.menu_id, m.name->>'en_US' as menu_name, g.id, g.name->>'en_US' as group_name
    FROM ir_ui_menu_group_rel rel
    JOIN ir_ui_menu m ON rel.menu_id = m.id
    JOIN res_groups g ON rel.gid = g.id
    WHERE rel.menu_id IN (394, 406, 407, 423, 430, 434);
''')
print("Menu explicit group restrictions:")
for r in cur.fetchall():
    print(r)

# Check all children of menu 423 (Medical CRM)
cur.execute('''
    SELECT m.id, m.name->>'en_US' as en, m.name->>'ar_001' as ar, m.parent_id, m.sequence, m.action
    FROM ir_ui_menu m
    WHERE m.parent_id = 423 OR m.parent_id = 430
    ORDER BY m.parent_id, m.sequence;
''')
print("\nMedical CRM Menus & Submenus:")
for r in cur.fetchall():
    print(r)

# Check all children of menu 394 (CRM)
cur.execute('''
    SELECT m.id, m.name->>'en_US' as en, m.name->>'ar_001' as ar, m.parent_id, m.sequence, m.action
    FROM ir_ui_menu m
    WHERE m.parent_id = 394 OR m.parent_id = 406
    ORDER BY m.parent_id, m.sequence;
''')
print("\nCRM Menus & Submenus:")
for r in cur.fetchall():
    print(r)

# Check res.config.settings views in DB
cur.execute('''
    SELECT v.id, v.name, v.inherit_id, imd.module, imd.name, v.arch_db
    FROM ir_ui_view v
    LEFT JOIN ir_model_data imd ON (imd.model = 'ir.ui.view' AND imd.res_id = v.id)
    WHERE v.model = 'res.config.settings'
    ORDER BY v.id;
''')
views = cur.fetchall()
print(f"\nTotal res.config.settings views: {len(views)}")
for v in views:
    mod = v[3] or ''
    name = v[4] or v[1]
    if 'medical' in mod or 'crm' in mod or 'crm' in name:
        print(f"View ID: {v[0]}, Name: {v[1]}, Inherit: {v[2]}, Module: {v[3]}, XMLID: {v[4]}")
        print("Arch:\n", v[5])
        print("-" * 50)
