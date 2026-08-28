import sys
sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Main company setup
    main_company = env['res.company'].browse(2)
    sa_country = env['res.country'].search([('code', '=', 'SA')], limit=1)
    
    if main_company.exists():
        main_company.write({
            'name': 'مجموعة الرعاية الطبية - Medical Care Group',
            'country_id': sa_country.id,
            'city': 'الرياض',
        })
        print(f"Main Company: {main_company.name} (ID: {main_company.id})")
    
    # 2. Setup the 5 Branches
    branches_data = [
        {'id': 3, 'name': 'فرع الرياض - Riyadh Branch', 'code': 'BR_RUH', 'city': 'الرياض', 'state_code': 'RUH'},
        {'id': 4, 'name': 'فرع جدة - Jeddah Branch', 'code': 'BR_JED', 'city': 'جدة', 'state_code': 'JED'},
        {'id': 5, 'name': 'فرع مكة المكرمة - Makkah Branch', 'code': 'BR_MAK', 'city': 'مكة المكرمة', 'state_code': 'MAK'},
        {'id': 6, 'name': 'فرع جازان - Jazan Branch', 'code': 'BR_GIZ', 'city': 'جازان', 'state_code': 'GIZ'},
        {'id': 7, 'name': 'فرع الطائف - Taif Branch', 'code': 'BR_TIF', 'city': 'الطائف', 'state_code': 'TIF'},
    ]
    
    branch_by_city = {}
    for b in branches_data:
        state = env['res.country.state'].search([('country_id', '=', sa_country.id), ('code', '=', b['state_code'])], limit=1)
        company = env['res.company'].browse(b['id'])
        company.write({
            'name': b['name'],
            'country_id': sa_country.id,
            'state_id': state.id if state else False,
            'city': b['city'],
        })
        branch_by_city[b['city']] = company
        print(f"Branch: {company.name} (ID: {company.id})")

    # 3. Setup the 4 Shared Medical Departments (medical.clinic)
    departments_data = [
        {
            'name': 'قسم الأسنان - Dental Department',
            'code': 'DENT',
            'specialty': 'Dental & Oral Health',
            'services': [
                {'name': 'تنظيف وتبييض الأسنان بجهاز زووم 4', 'code': 'ZOOM4', 'price': 600.0, 'type': 'service'},
                {'name': 'ابتسامة هوليوود 3D (عدسات E-max لـ 16 سناً)', 'code': 'EMAX16', 'price': 8000.0, 'type': 'service'},
                {'name': 'زراعة الأسنان الألمانية الفورية مع تاج الزيركون', 'code': 'IMPLANT_GER', 'price': 2500.0, 'type': 'service'},
                {'name': 'تقويم الأسنان الشفاف (Invisalign)', 'code': 'INVISALIGN', 'price': 9000.0, 'type': 'consultation'},
                {'name': 'علاج عصب الأسنان المجهري بجلسة واحدة', 'code': 'ROOT_CANAL', 'price': 700.0, 'type': 'service'},
                {'name': 'الخلع الجراحي لضرس العقل المدفون', 'code': 'WISDOM_EXT', 'price': 800.0, 'type': 'service'},
            ]
        },
        {
            'name': 'قسم الليزر - Laser Department',
            'code': 'LASER',
            'specialty': 'Laser & Skin Care',
            'services': [
                {'name': 'باقة ليزر جسم كامل مع الرتوش', 'code': 'LASER_FB', 'price': 450.0, 'type': 'service'},
                {'name': 'جلسة ليزر كربوني لنضارة الوجه', 'code': 'CARBON_LASER', 'price': 300.0, 'type': 'service'},
                {'name': 'جلسة هيدرافيشل لتنظيف البشرة العميق', 'code': 'HYDRAFACIAL', 'price': 350.0, 'type': 'service'},
                {'name': 'جلسة شد وتحديد الوجه هايفو (HIFU)', 'code': 'HIFU_FACE', 'price': 1200.0, 'type': 'service'},
                {'name': 'حقن الفيلر للشفايف والخدود 1 مل', 'code': 'FILLER_1ML', 'price': 950.0, 'type': 'service'},
                {'name': 'حقن البوتوكس للتجاعيد وكامل الوجه', 'code': 'BOTOX_FACE', 'price': 850.0, 'type': 'service'},
            ]
        },
        {
            'name': 'قسم زراعة الشعر - Hair Transplant Department',
            'code': 'HAIR',
            'specialty': 'Hair Restoration',
            'services': [
                {'name': 'زراعة الشعر بالاقتطاف الدقيق FUE لـ 3000 بصيلة', 'code': 'FUE_3000', 'price': 6500.0, 'type': 'service'},
                {'name': 'جلسة بلازما ماجلان للشعر والبشرة', 'code': 'MAGELLAN_PRP', 'price': 900.0, 'type': 'service'},
                {'name': 'زراعة شعر اللحية والشارب', 'code': 'BEARD_TRANS', 'price': 4500.0, 'type': 'service'},
                {'name': 'علاج تساقط الشعر بالميزوثيرابي', 'code': 'MESO_HAIR', 'price': 500.0, 'type': 'service'},
            ]
        },
        {
            'name': 'قسم الجراحة التجميلية - Plastic Surgery Department',
            'code': 'SURG',
            'specialty': 'Plastic & Reconstructive Surgery',
            'services': [
                {'name': 'شفط الدهون ونحت القوام بالفيزر VASER', 'code': 'VASER_LIPO', 'price': 12000.0, 'type': 'consultation'},
                {'name': 'تجميل وتعديل مسار الأنف Rhinoplasty', 'code': 'RHINOPLASTY', 'price': 14000.0, 'type': 'consultation'},
                {'name': 'عملية شد البطن Tummy Tuck', 'code': 'TUMMY_TUCK', 'price': 16000.0, 'type': 'consultation'},
                {'name': 'شد وتجميل الجفون Blepharoplasty', 'code': 'BLEPHARO', 'price': 6000.0, 'type': 'service'},
            ]
        },
    ]

    # Clear old services & clinics
    env['medical.service'].search([]).unlink()
    env['medical.clinic'].search([]).unlink()

    dept_by_code = {}
    service_by_name = {}

    for d in departments_data:
        clinic = env['medical.clinic'].create({
            'name': d['name'],
            'code': d['code'],
            'specialty': d['specialty'],
            'company_id': False,  # Shared across all branches
            'active': True,
        })
        dept_by_code[d['code']] = clinic
        print(f"Created Shared Department: {clinic.name} (ID: {clinic.id})")
        
        for s in d['services']:
            srv = env['medical.service'].create({
                'name': s['name'],
                'code': s['code'],
                'clinic_id': clinic.id,
                'price': s['price'],
                'consultation_type': s['type'],
                'active': True,
            })
            service_by_name[s['name']] = srv

    print(f"Total Services created: {len(service_by_name)}")

    # 4. Update all 82 Leads in CRM
    leads = env['crm.lead'].search([])
    for lead in leads:
        # Match Branch
        branch = branch_by_city.get(lead.city_name) or branch_by_city.get('الرياض')
        
        # Match Service & Department
        matched_srv = None
        for s_name, srv in service_by_name.items():
            keywords = s_name.split()[:2]
            if any(k in lead.name for k in keywords if len(k) > 3):
                matched_srv = srv
                break
                
        if not matched_srv:
            if any(k in lead.name for k in ['ليزر', 'بشرة', 'فيلر', 'بوتوكس', 'هيدرافيشل', 'هايفو']):
                dept = dept_by_code['LASER']
            elif any(k in lead.name for k in ['أسنان', 'تقويم', 'تبييض', 'زراعة', 'عصب', 'ضرس', 'ابتسامة']):
                dept = dept_by_code['DENT']
            elif any(k in lead.name for k in ['شعر', 'صلع', 'بلازما', 'لحية']):
                dept = dept_by_code['HAIR']
            else:
                dept = dept_by_code['LASER']
            matched_srv = env['medical.service'].search([('clinic_id', '=', dept.id)], limit=1)

        lead.write({
            'branch_id': branch.id if branch else False,
            'clinic_id': matched_srv.clinic_id.id if matched_srv else False,
            'service_id': matched_srv.id if matched_srv else False,
            'expected_revenue': matched_srv.price if matched_srv else 0.0,
        })

    cr.commit()
    print("SUCCESS: All leads updated successfully with Branches, Shared Departments and Services.")
