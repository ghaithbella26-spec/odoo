import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# 1. Activate ar_001
cur.execute("UPDATE res_lang SET active = true WHERE code = 'ar_001'")

# 2. Update partners of active users to ar_001
cur.execute("UPDATE res_partner SET lang = 'ar_001'")

conn.commit()

cur.execute("""
    SELECT u.login, p.lang 
    FROM res_users u 
    JOIN res_partner p ON u.partner_id = p.id 
    WHERE u.active = true
""")
print("=== ACTIVE USERS LANGUAGE AFTER UPDATE ===")
for r in cur.fetchall():
    print(f"User: {r[0]} -> Lang: {r[1]}")

conn.close()
