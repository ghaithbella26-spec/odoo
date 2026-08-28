import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

cur.execute('''
    SELECT u.id, u.login, p.name, u.write_date
    FROM res_users u
    JOIN res_partner p ON u.partner_id = p.id
    ORDER BY u.write_date DESC;
''')
print("Users by last update:")
for r in cur.fetchall():
    print(r)
