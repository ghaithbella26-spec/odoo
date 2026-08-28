import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {'lang': 'ar_001'})
    
    # ----------------------------------------------------
    # 1. TRANSLATING & REFINING CRM STAGES & SLA HOURS
    # ----------------------------------------------------
    stage_configs = [
        {'id': 57, 'name': 'فرصة جديدة - New Lead', 'sla': 2.0, 'prob': 10.0, 'seq': 10},
        {'id': 63, 'name': 'مؤهل للاستشارة - Qualified', 'sla': 24.0, 'prob': 30.0, 'seq': 20},
        {'id': 65, 'name': 'تم حجز الموعد - Appointment Booked', 'sla': 48.0, 'prob': 60.0, 'seq': 30},
        {'id': 66, 'name': 'زار العيادة والكشف - Visited Clinic', 'sla': 48.0, 'prob': 80.0, 'seq': 40},
        {'id': 70, 'name': 'خطة العلاج والإجراء - Treatment', 'sla': 168.0, 'prob': 90.0, 'seq': 50},
        {'id': 69, 'name': 'تم بنجاح (فوز) - Won', 'sla': 0.0, 'prob': 100.0, 'seq': 60},
    ]
    
    for s in stage_configs:
        stage = env['crm.stage'].browse(s['id'])
        if stage.exists():
            stage.write({
                'name': s['name'],
                'sla_hours': s['sla'],
                'sequence': s['seq'],
            })
            print(f"Refined Stage: {stage.name} -> SLA: {stage.sla_hours}h")

    # ----------------------------------------------------
    # 2. TRANSLATING & REFINING ACTIVITY TYPES
    # ----------------------------------------------------
    activities = [
        {
            'name': 'اتصال كول سنتر - Call Center Call',
            'category': 'phonecall',
            'icon': 'fa-phone',
            'delay_count': 0,
            'delay_unit': 'days',
            'summary': 'الاتصال الأولي بالمريض وفحص الاحتياج الطبي',
            'default_note': 'التحقق من الخدمة المطلوبة، توضيح العروض، وعرض مواعيد الاستشارة المتاحة بالعيادة.',
        },
        {
            'name': 'تأكيد موعد عيادة - Appointment Confirmation',
            'category': 'default',
            'icon': 'fa-calendar-check-o',
            'delay_count': 1,
            'delay_unit': 'days',
            'summary': 'تأكيد حضور الموعد بالعيادة وإرسال موقع الفرع',
            'default_note': 'التواصل مع المريض لتأكيد الحضور، وإرسال موقع الفرع عبر الواتساب.',
        },
        {
            'name': 'متابعة ما بعد العلاج - Post-Treatment Follow-up',
            'category': 'default',
            'icon': 'fa-heartbeat',
            'delay_count': 3,
            'delay_unit': 'days',
            'summary': 'متابعة رضا المريض والاطمئنان بعد الإجراء الطبي',
            'default_note': 'الاطمئنان على المريض بعد جلسة العلاج، قياس مدى الرضا، وجدولة جلسة الرتوش إن وجدت.',
        }
    ]
    
    for act in activities:
        rec = env['mail.activity.type'].search(['|', ('name', '=', act['name']), ('name', 'ilike', act['name'].split()[0])], limit=1)
        if rec:
            rec.write(act)
        else:
            env['mail.activity.type'].create(act)
    print("Refined Activity Types successfully.")

    # ----------------------------------------------------
    # 3. TRANSLATING & REFINING LOST REASONS
    # ----------------------------------------------------
    lost_reasons = [
        'السعر مرتفع مقارنة بالميزانية',
        'موقع الفرع أو العيادة بعيد',
        'تم الحجز والعلاج لدى مركز طبي آخر',
        'عدم الرد على اتصالات ورسائل الكول سنتر',
        'غير جاد أو غير مهتم حالياً',
        'الخدمة الطبية المطلوبة غير متوفرة',
    ]
    for lr_name in lost_reasons:
        lr = env['crm.lost.reason'].search([('name', '=', lr_name)], limit=1)
        if not lr:
            env['crm.lost.reason'].create({'name': lr_name})
    print(f"Ensured {len(lost_reasons)} Lost Reasons in Arabic.")

    # ----------------------------------------------------
    # 4. TRANSLATING MEDICAL CRM MENUS IN ARABIC
    # ----------------------------------------------------
    menu_translations = {
        'Medical CRM': 'إدارة علاقات المرضى (Medical CRM)',
        'Pipelines': 'خط الأنابيب ومتابعة المرضى',
        'Call Center Workspace': 'مساحة عمل الكول سنتر',
        'Distribution Rules': 'قواعد التوزيع التلقائي',
        'API Settings': 'إعدادات الـ API والربط',
        'Platforms': 'منصات الإعلانات والتواصل',
        'Clinics': 'الأقسام والعيادات التخصصية',
        'Services': 'الخدمات والإجراءات الطبية',
        'Batches': 'دفعات الاستيراد والحملات',
        'User Roles': 'أدوار وصلاحيات المستخدمين',
        'Call Logs': 'سجلات المكالمات والاتصالات',
        'Audit Logs': 'سجلات التدقيق والأمان',
        'API Logs': 'سجلات الـ Webhooks والـ API',
        'Campaign ROI Report': 'تقرير العائد على الحملات (ROI)',
        'Agent Performance': 'تقرير أداء موظفي الكول سنتر',
        'Medical Funnel Analysis': 'تحليل قمع التحويل الطبي (Funnel)',
        'Medical CRM Analysis': 'تحليل المبيعات والخدمات الطبية',
    }

    for en_name, ar_name in menu_translations.items():
        menus = env['ir.ui.menu'].search(['|', ('name', '=', en_name), ('name', '=', ar_name)])
        for m in menus:
            m.write({'name': ar_name})
            print(f"Updated Menu ID {m.id} -> {ar_name}")

    cr.commit()
    print("\nSUCCESS: All translations and procedural data updated successfully.")
