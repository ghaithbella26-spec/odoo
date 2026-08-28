import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Target 3 Medical Activity Types
    activities = [
        {
            'name': 'اتصال كول سنتر - Call Center Call',
            'category': 'phonecall',
            'icon': 'fa-phone',
            'delay_count': 0,
            'delay_unit': 'days',
            'delay_from': 'current_date',
            'summary': 'الاتصال الأولي بالمريض لفحص الاحتياج الطبي',
            'default_note': 'التحقق من الخدمة المطلوبة، توضيح العروض الطبية، وحجز موعد كشف بالعيادة.',
        },
        {
            'name': 'تأكيد موعد عيادة - Appointment Confirmation',
            'category': 'default',
            'icon': 'fa-calendar-check-o',
            'delay_count': 1,
            'delay_unit': 'days',
            'delay_from': 'previous_activity',
            'summary': 'تأكيد حضور الموعد بالعيادة وإرسال اللوكيشن',
            'default_note': 'التواصل مع المريض لتأكيد الحضور غداً، وإرسال موقع الفرع عبر الواتساب.',
        },
        {
            'name': 'متابعة ما بعد العلاج - Post-Treatment Follow-up',
            'category': 'default',
            'icon': 'fa-heartbeat',
            'delay_count': 3,
            'delay_unit': 'days',
            'delay_from': 'previous_activity',
            'summary': 'متابعة رضا المريض والاطمئنان بعد الإجراء الطبي',
            'default_note': 'الاطمئنان على صحة المريض بعد جلسة الليزر / الإجراء الطبي، وقياس مستوى الرضا وجدولة الرتوش.',
        }
    ]
    
    for act in activities:
        rec = env['mail.activity.type'].search(['|', ('name', '=', act['name']), ('name', 'ilike', act['name'].split()[0])], limit=1)
        if rec:
            rec.write(act)
            print(f"Updated Activity: {rec.name} (ID: {rec.id})")
        else:
            rec = env['mail.activity.type'].create(act)
            print(f"Created Activity: {rec.name} (ID: {rec.id})")

    cr.commit()
    print("SUCCESS: Medical Activity Types configured successfully.")
