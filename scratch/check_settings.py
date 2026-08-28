import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# Get users
cur.execute('''
    SELECT u.id, u.login, p.name 
    FROM res_users u 
    LEFT JOIN res_partner p ON u.partner_id = p.id;
''')
print("Users:", cur.fetchall())

# Check all groups for admin
cur.execute('''
    SELECT g.id, g.name->>'en_US' as name_en, g.name->>'ar_001' as name_ar, imd.module, imd.name as xml_id
    FROM res_groups_users_rel rel
    JOIN res_groups g ON rel.gid = g.id
    LEFT JOIN ir_model_data imd ON (imd.model = 'res.groups' AND imd.res_id = g.id)
    JOIN res_users u ON rel.uid = u.id
    WHERE u.login = 'admin'
    ORDER BY imd.module, imd.name;
''')
admin_groups = cur.fetchall()
print(f"\nAdmin has {len(admin_groups)} groups.")
print("Admin groups:")
for g in admin_groups:
    print(f" - {g[3]}.{g[4]}: {g[1]} / {g[2]}")

# Check CRM menus
cur.execute('''
    SELECT m.id, m.name->>'en_US', m.name->>'ar_001', m.parent_id, imd.module, imd.name
    FROM ir_ui_menu m
    LEFT JOIN ir_model_data imd ON (imd.model = 'ir.ui.menu' AND imd.res_id = m.id)
    WHERE m.name->>'en_US' ILIKE '%crm%' OR m.name->>'en_US' ILIKE '%config%' OR m.name->>'en_US' ILIKE '%setting%'
       OR m.name->>'ar_001' ILIKE '%تهيئة%' OR m.name->>'ar_001' ILIKE '%إعدادات%'
    ORDER BY m.parent_id, m.sequence;
''')
print("\nRelevant Menus:")
for m in cur.fetchall():
    print(m)
