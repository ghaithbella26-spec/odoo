import psycopg2
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(host='localhost', port=5432, user='odoo', password='odoo', dbname='dbodoo18')
cur = conn.cursor()

# Translation dictionary mapping english terms to perfect professional Arabic
translations_dict = {
    # Main Apps & Top Menus
    "Medical CRM": "إدارة علاقات المرضى (Medical CRM)",
    "CRM": "إدارة علاقات العملاء (CRM)",
    "Sales": "المبيعات",
    "Leads": "الفرص والليدات",
    "Pipeline": "خط الأنابيب والمتابعة",
    "My Pipeline": "خط المتابعة الخاص بي",
    "My Leads": "مرضاي وليداتي",
    "Lead Batches": "دفعات الليدات والحملات",
    "Clinics": "الأقسام والعيادات التخصصية",
    "Services": "الخدمات والإجراءات الطبية",
    "Reports": "التقارير والإحصائيات",
    "Reporting": "التقارير",
    "Platforms": "منصات الإعلانات",
    "API & Integration": "الربط البرمجي والـ API",
    "Call Center": "مركز الاتصال (الكول سنتر)",
    "Configuration": "التهيئة والإعدادات",
    "Settings": "الإعدادات العامة",
    "Generate Leads": "توليد ليدات جديدة",
    "Import Leads": "استيراد ليدات",
    "Lead Generation": "توليد الفرص",
    "Lead Mining Requests": "طلبات استخراج الليدات",
    "Lead Analysis": "تحليل أداء الليدات",
    "Pipeline Stages": "مراحل خط الأنابيب",
    "Stages": "المراحل",
    "Tags": "الوسوم والتصنيفات",
    "Lost Reasons": "أسباب خسارة الفرص",
    "Activity Types": "أنواع الأنشطة والمتابعات",
    "Sales Teams": "فرق المبيعات والكول سنتر",
    "Teams": "فرق العمل",
    "Customers": "سجل المرضى والعملاء",
    "My Activities": "أنشطتي ومواعيدي",
    "My Quotations": "عروضي السعرية",
    "Activities": "الأنشطة المجدولة",
    "Forecast": "توقعات الإيرادات",
    "Campaigns": "الحملات التسويقية",
    "UTM Campaigns": "الحملات الإعلانية (UTM)",
    "UTM Sources": "مصادر الزيارات (Sources)",
    "UTM Mediums": "وسائط الحملات (Mediums)",

    # Medical Custom Menus & Actions
    "Call Center Workspace": "مساحة عمل الكول سنتر",
    "Call Logs": "سجلات المكالمات والاتصالات",
    "Distribution Rules": "قواعد التوزيع التلقائي",
    "API Settings": "إعدادات الربط والـ API",
    "API Logs": "سجلات الـ Webhooks والـ API",
    "Audit Logs": "سجلات التدقيق والأمان",
    "User Roles": "أدوار وصلاحيات المستخدمين",
    "Campaign ROI Report": "تقرير العائد على الحملات (ROI)",
    "Agent Performance": "تقرير أداء موظفي الكول سنتر",
    "Medical Funnel Analysis": "تحليل قمع التحويل الطبي (Funnel)",
    "Medical CRM Analysis": "تحليل المبيعات والخدمات الطبية",
    "Medical Clinics": "الأقسام والعيادات التخصصية",
    "Medical Services": "الخدمات والإجراءات الطبية",
    "Medical Platforms": "منصات الإعلانات والتواصل",
    "Lead Batch Import": "استيراد دفعة ليدات",

    # Window Actions
    "API Configuration": "إعدادات الربط البرمجي والـ Webhooks",
    "Medical Leads": "فرص المرضى والليدات",
    "Opportunity": "فرصة المريض",
    "Opportunities": "فرص المرضى والمبيعات",
    "Medical Services List": "قائمة الخدمات الطبية",
    "Medical Clinics List": "قائمة الأقسام التخصصية",
    "Call Logs History": "سجل مكالمات الكول سنتر",
    "Distribution Rules Engine": "محرك قواعد التوزيع الذكي",
    "ROI Report": "تقرير العائد الاستثماري",
    "Agent Performance Report": "تقرير إنتاجية الوكلاء",
    "Medical Funnel": "قمع التحويل الطبي",

    # Stages
    "New Lead": "فرصة جديدة",
    "Qualified": "مؤهل للاستشارة",
    "Appointment Booked": "تم حجز الموعد",
    "Visited Clinic": "زار العيادة والكشف",
    "Treatment": "خطة العلاج والإجراء",
    "Won": "تم بنجاح (فوز)",
    "Lost": "خسارة / مستبعد",

    # Activities
    "Email": "بريد إلكتروني",
    "Call": "اتصال هاتفي",
    "Meeting": "موعد / مقابلة",
    "To-Do": "مهمة للمتابعة",
    "Upload Document": "رفع مستند / ملف",
    "Follow-up Quote": "متابعة عرض السعر",
    "Make Quote": "إعداد عرض سعر",
    "Call for Demo": "مكالمة توضيحية",
    "Order Upsell": "ترقية الخدمة / مبيعات إضافية",
    "Call Center Call": "اتصال كول سنتر",
    "Appointment Confirmation": "تأكيد موعد عيادة",
    "Post-Treatment Follow-up": "متابعة ما بعد العلاج",
}

# 1. Update ir_ui_menu table
cur.execute("SELECT id, name FROM ir_ui_menu WHERE name IS NOT NULL")
menus = cur.fetchall()
updated_menus = 0

for menu_id, name_json in menus:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '')
        # Check direct match or stripped match
        ar_val = translations_dict.get(en_val) or translations_dict.get(en_val.strip())
        
        # If not found directly, check partial matches
        if not ar_val:
            for k, v in translations_dict.items():
                if k.lower() == en_val.lower().strip():
                    ar_val = v
                    break
                    
        if ar_val:
            name_json['ar_001'] = ar_val
            cur.execute("UPDATE ir_ui_menu SET name = %s WHERE id = %s", (json.dumps(name_json), menu_id))
            updated_menus += 1

print(f"Updated {updated_menus} Menus with Arabic translations.")

# 2. Update ir_act_window table
cur.execute("SELECT id, name FROM ir_act_window WHERE name IS NOT NULL")
actions = cur.fetchall()
updated_actions = 0

for act_id, name_json in actions:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '')
        ar_val = translations_dict.get(en_val) or translations_dict.get(en_val.strip())
        if not ar_val:
            for k, v in translations_dict.items():
                if k.lower() == en_val.lower().strip():
                    ar_val = v
                    break
        if ar_val:
            name_json['ar_001'] = ar_val
            cur.execute("UPDATE ir_act_window SET name = %s WHERE id = %s", (json.dumps(name_json), act_id))
            updated_actions += 1

print(f"Updated {updated_actions} Window Actions with Arabic translations.")

# 3. Update crm_stage table
cur.execute("SELECT id, name FROM crm_stage WHERE name IS NOT NULL")
stages = cur.fetchall()
for stg_id, name_json in stages:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '')
        ar_val = None
        if 'new' in en_val.lower(): ar_val = 'فرصة جديدة'
        elif 'qualif' in en_val.lower(): ar_val = 'مؤهل للاستشارة'
        elif 'book' in en_val.lower(): ar_val = 'تم حجز الموعد'
        elif 'visit' in en_val.lower(): ar_val = 'زار العيادة والكشف'
        elif 'treat' in en_val.lower(): ar_val = 'خطة العلاج والإجراء'
        elif 'won' in en_val.lower() or 'فوز' in en_val: ar_val = 'تم بنجاح (فوز)'
        
        if ar_val:
            name_json['ar_001'] = ar_val
            cur.execute("UPDATE crm_stage SET name = %s WHERE id = %s", (json.dumps(name_json), stg_id))

print("Updated CRM Stages translations.")

# 4. Update mail_activity_type table
cur.execute("SELECT id, name FROM mail_activity_type WHERE name IS NOT NULL")
acts = cur.fetchall()
for act_id, name_json in acts:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '')
        ar_val = translations_dict.get(en_val)
        if not ar_val:
            if 'phone' in en_val.lower() or 'call' in en_val.lower():
                if 'center' in en_val.lower(): ar_val = 'اتصال كول سنتر'
                else: ar_val = 'مكالمة هاتفية'
            elif 'confirm' in en_val.lower(): ar_val = 'تأكيد موعد عيادة'
            elif 'post' in en_val.lower() or 'follow' in en_val.lower(): ar_val = 'متابعة ما بعد العلاج'
            elif 'email' in en_val.lower(): ar_val = 'بريد إلكتروني'
            elif 'meet' in en_val.lower(): ar_val = 'موعد بالعيادة'
            elif 'todo' in en_val.lower() or 'to-do' in en_val.lower(): ar_val = 'مهمة متابعة'
        if ar_val:
            name_json['ar_001'] = ar_val
            cur.execute("UPDATE mail_activity_type SET name = %s WHERE id = %s", (json.dumps(name_json), act_id))

print("Updated Activity Types translations.")

# 5. Update medical_clinic & medical_service
cur.execute("SELECT id, name FROM medical_clinic WHERE name IS NOT NULL")
clinics = cur.fetchall()
for cid, name_json in clinics:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '')
        if 'dent' in en_val.lower() or 'أسنان' in en_val:
            name_json['ar_001'] = 'قسم الأسنان'
        elif 'laser' in en_val.lower() or 'ليزر' in en_val:
            name_json['ar_001'] = 'قسم الليزر والعناية بالبشرة'
        elif 'hair' in en_val.lower() or 'شعر' in en_val:
            name_json['ar_001'] = 'قسم زراعة الشعر'
        elif 'surg' in en_val.lower() or 'جراح' in en_val:
            name_json['ar_001'] = 'قسم الجراحة التجميلية'
        cur.execute("UPDATE medical_clinic SET name = %s WHERE id = %s", (json.dumps(name_json), cid))

cur.execute("SELECT id, name FROM medical_service WHERE name IS NOT NULL")
services = cur.fetchall()
for sid, name_json in services:
    if isinstance(name_json, dict):
        en_val = name_json.get('en_US', '')
        name_json['ar_001'] = en_val  # already in Arabic in our seed
        cur.execute("UPDATE medical_service SET name = %s WHERE id = %s", (json.dumps(name_json), sid))

# 6. Update res_users_role
cur.execute("SELECT id, name, code FROM res_users_role WHERE name IS NOT NULL")
roles = cur.fetchall()
role_translations = {
    'CC_AGENT': 'موظف كول سنتر',
    'CC_SUPERVISOR': 'مشرف كول سنتر',
    'BRANCH_MGR': 'مدير فرع وعيادة',
    'MARKETING_SPEC': 'أخصائي تسويق وحملات',
    'CRM_ADMIN': 'مدير النظام الطبي (Admin)',
}
for rid, name_json, code in roles:
    if isinstance(name_json, dict) and code in role_translations:
        name_json['ar_001'] = role_translations[code]
        cur.execute("UPDATE res_users_role SET name = %s WHERE id = %s", (json.dumps(name_json), rid))

conn.commit()
conn.close()
print("SUCCESS: All JSONB translations updated for ar_001 across the system!")
