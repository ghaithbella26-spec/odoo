import psycopg2
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# Idiomatic, contextual Arabic medical & business terms (معنى سياقي طبي وليس ترجمة حرفية)
contextual_translations = {
    # Main Apps & Top Menus
    "Medical CRM": "إدارة علاقات المرضى",
    "CRM": "إدارة المبيعات والعملاء",
    "Sales": "المبيعات",
    "Leads": "طلبات الحجز والاستفسارات",
    "Pipeline": "مسار رحلة المريض",
    "My Pipeline": "متابعاتي اليومية",
    "My Leads": "المرضى المسندين لي",
    "Lead Batches": "قوائم الحملات الإعلانية",
    "Clinics": "العيادات التخصصية",
    "Services": "الخدمات والعمليات الطبية",
    "Reports": "مؤشرات الأداء والتقارير",
    "Reporting": "التقارير",
    "Platforms": "القنوات الإعلانية",
    "API & Integration": "الربط مع الإعلانات والـ API",
    "Call Center": "مركز الاتصال",
    "Configuration": "إعدادات النظام",
    "Settings": "الإعدادات العامة",
    "Generate Leads": "استقطاب مهتمين جدد",
    "Import Leads": "استيراد أرقام وقوائم",
    "Lead Generation": "استقطاب المرضى",
    "Lead Mining Requests": "طلبات البحث عن عملاء",
    "Lead Analysis": "تحليل مصادر المرضى",
    "Pipeline Stages": "مراحل مسار المتابعة",
    "Stages": "مراحل الحجز",
    "Tags": "تصنيفات واهتمامات المرضى",
    "Lost Reasons": "أسباب عدم إتمام الحجز",
    "Activity Types": "أنواع المتابعات والمواعيد",
    "Sales Teams": "فرق الحجز والاستقبال",
    "Teams": "فرق العمل",
    "Customers": "سجل المرضى",
    "My Activities": "مهامي ومواعيدي اليوم",
    "My Quotations": "خطط الأسعار والعروض",
    "Activities": "المتابعات المجدولة",
    "Forecast": "توقعات الإيرادات",
    "Campaigns": "الحملات التسويقية",
    "UTM Campaigns": "الحملات الترويجية",
    "UTM Sources": "مصادر وصول المرضى",
    "UTM Mediums": "وسائط الإعلانات",

    # Medical Menus & Actions
    "Call Center Workspace": "لوحة استقبال واتصال المرضى",
    "Call Logs": "سجل مكالمات المرضى",
    "Distribution Rules": "قواعد توجيه المرضى آلياً",
    "API Settings": "إعدادات استقبال الإعلانات",
    "API Logs": "سجل استقبال الإعلانات الفورية",
    "Audit Logs": "سجل الأمان والعمليات",
    "User Roles": "صلاحيات ومسميات الموظفين",
    "Campaign ROI Report": "العائد المالي على الإعلانات (ROI)",
    "Agent Performance": "إنتاجية موظفي الكول سنتر",
    "Medical Funnel Analysis": "تحليل نسب تحويل المرضى (Funnel)",
    "Medical CRM Analysis": "تحليل مبيعات الخدمات الطبية",
    "Medical Clinics": "العيادات التخصصية",
    "Medical Services": "الخدمات والإجراءات الطبية",
    "Medical Platforms": "القنوات والمنصات الإعلانية",
    "Lead Batch Import": "استيراد قائمة حملة إعلانية",
    "API Configuration": "إعدادات نقاط الربط الإعلاني",
    "Medical Leads": "طلبات واستفسارات المرضى",
    "Opportunity": "ملف متابعة المريض",
    "Opportunities": "متابعات الحجز والعلاج",
}

# 1. Update ir_ui_menu
cur.execute("SELECT id, name FROM ir_ui_menu WHERE name IS NOT NULL")
menus = cur.fetchall()
for menu_id, name_json in menus:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '').strip()
        ar_val = contextual_translations.get(en_val)
        if not ar_val:
            for k, v in contextual_translations.items():
                if k.lower() == en_val.lower():
                    ar_val = v
                    break
        if ar_val:
            name_json['ar_001'] = ar_val
            cur.execute("UPDATE ir_ui_menu SET name = %s WHERE id = %s", (json.dumps(name_json), menu_id))

# 2. Update ir_act_window
cur.execute("SELECT id, name FROM ir_act_window WHERE name IS NOT NULL")
actions = cur.fetchall()
for act_id, name_json in actions:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '').strip()
        ar_val = contextual_translations.get(en_val)
        if not ar_val:
            for k, v in contextual_translations.items():
                if k.lower() == en_val.lower():
                    ar_val = v
                    break
        if ar_val:
            name_json['ar_001'] = ar_val
            cur.execute("UPDATE ir_act_window SET name = %s WHERE id = %s", (json.dumps(name_json), act_id))

# 3. Update Stages with context-driven medical terms
stages_map = {
    57: {'en_US': 'New Lead', 'ar_001': 'طلب جديد (بانتظار التواصل)'},
    63: {'en_US': 'Qualified', 'ar_001': 'تم التواصل وفحص الاحتياج'},
    65: {'en_US': 'Appointment Booked', 'ar_001': 'تم تأكيد الموعد بالعيادة'},
    66: {'en_US': 'Visited Clinic', 'ar_001': 'حضر للعيادة وأتم الكشف'},
    70: {'en_US': 'Treatment', 'ar_001': 'بدء الجلسات والعلاج'},
    69: {'en_US': 'Won', 'ar_001': 'تم إتمام الخدمة بنجاح'},
}
for sid, vals in stages_map.items():
    cur.execute("UPDATE crm_stage SET name = %s WHERE id = %s", (json.dumps(vals), sid))

# 4. Update Activities with natural medical terms
acts_map = {
    'Call Center Call': {'en': 'Call Center Call', 'ar': 'اتصال هاتفي أول'},
    'Appointment Confirmation': {'en': 'Appointment Confirmation', 'ar': 'تأكيد حضور الموعد'},
    'Post-Treatment Follow-up': {'en': 'Post-Treatment Follow-up', 'ar': 'متابعة واطمئنان بعد الإجراء'},
}
for act_key, val in acts_map.items():
    cur.execute("SELECT id, name FROM mail_activity_type WHERE name::text ILIKE %s", (f"%{act_key}%",))
    for r in cur.fetchall():
        cur.execute("UPDATE mail_activity_type SET name = %s WHERE id = %s", (json.dumps({'en_US': val['en'], 'ar_001': val['ar']}), r[0]))

# 5. Update Lost Reasons to context-driven terms
cur.execute("DELETE FROM crm_lost_reason")
lost_reasons = [
    'السعر غير مناسب للمريض',
    'موقع الفرع بعيد عن المريض',
    'حجز وتلقى العلاج في مركز آخر',
    'تعذر الوصول للمريض (لا يرد)',
    'متردد / أجل القرار لوقت لاحق',
    'الخدمة أو التخصص غير متوفر لدينا',
]
for lr in lost_reasons:
    cur.execute("INSERT INTO crm_lost_reason (name, active) VALUES (%s, true)", (json.dumps({'en_US': lr, 'ar_001': lr}),))

# 6. Update User Roles
roles_map = {
    'CC_AGENT': 'أخصائي خدمة عملاء وحجز',
    'CC_SUPERVISOR': 'مشرف مركز الاتصال',
    'BRANCH_MGR': 'مدير الفرع والعيادات',
    'MARKETING_SPEC': 'مسؤول الحملات التسويقية',
    'CRM_ADMIN': 'مدير المنظومة الطبية',
}
for code, title in roles_map.items():
    cur.execute("UPDATE res_users_role SET name = %s WHERE code = %s", (json.dumps({'en_US': title, 'ar_001': title}), code))

conn.commit()
conn.close()
print("SUCCESS: Context-driven, natural medical Arabic translations applied successfully!")
