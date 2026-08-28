import psycopg2
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# Update action name and menu name
cur.execute("""
    UPDATE ir_act_window 
    SET name = %s 
    WHERE id = 682
""", (json.dumps({'en_US': 'Medical App Launcher', 'ar_001': 'الرئيسية - بوابة التطبيقات الطبية'}),))

cur.execute("""
    UPDATE ir_ui_menu 
    SET name = %s 
    WHERE id = 459
""", (json.dumps({'en_US': 'Home', 'ar_001': 'الرئيسية'}),))

conn.commit()
conn.close()
print("Updated Launcher names in Arabic.")
