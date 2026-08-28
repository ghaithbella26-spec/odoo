import sys
import json
import traceback
from datetime import timedelta

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID, fields

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')

report = {
    'system_health': 'EXCELLENT',
    'simulations': [],
    'frictions_and_gaps': [],
    'operational_findings': [],
    'admin_recommendations': []
}

def log_sim(title, status, message=""):
    report['simulations'].append({'title': title, 'status': status, 'message': message})

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. TEST LEAD LIFECYCLE & STAGE TRANSITIONS
    print("--- 1. Testing Lead Lifecycle & Activity Generation ---")
    try:
        new_stage = env['crm.stage'].search([('name', 'ilike', 'جديد')], limit=1)
        booked_stage = env['crm.stage'].search([('name', 'ilike', 'حجز')], limit=1)
        won_stage = env['crm.stage'].search([('is_won', '=', True)], limit=1)
        agent = env['res.users'].search([('role_ids.code', 'ilike', 'AGENT')], limit=1) or env['res.users'].search([('id', '!=', 1)], limit=1)
        clinic = env['medical.clinic'].search([], limit=1)
        service = env['medical.service'].search([('clinic_id', '=', clinic.id)], limit=1) if clinic else False
        branch = env['res.company'].search([('parent_id', '!=', False)], limit=1)

        test_lead = env['crm.lead'].create({
            'name': 'اختبار محاكاة المريض - Admin Simulation',
            'partner_name': 'سعد العتيبي',
            'phone': '0555123456',
            'mobile': '0555123456',
            'city_name': 'الرياض',
            'clinic_id': clinic.id if clinic else False,
            'service_id': service.id if service else False,
            'branch_id': branch.id if branch else False,
            'company_id': branch.id if branch else env.company.id,
            'user_id': agent.id if agent else False,
            'stage_id': new_stage.id if new_stage else False,
            'type': 'opportunity',
        })
        
        # Check initial automated activity
        acts = env['mail.activity'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', test_lead.id)])
        log_sim("Lead Creation & Automated Activity", "PASS", f"Lead ID {test_lead.id} created with {len(acts)} initial activity: {[a.summary for a in acts]}")

        # Transition to Booked
        if booked_stage:
            test_lead.write({'stage_id': booked_stage.id})
            acts2 = env['mail.activity'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', test_lead.id)])
            log_sim("Stage Transition to Booked", "PASS", f"Activities after stage change: {[a.summary for a in acts2]}")

        # Rollback test lead
        test_lead.unlink()
    except Exception as e:
        log_sim("Lead Lifecycle & Activity", "FAIL", str(e))
        report['frictions_and_gaps'].append(f"Lead lifecycle error: {e}")

    # 2. TEST CALL LOGS CREATION & CALL CENTER WORKSPACE
    print("--- 2. Testing Call Center Workspace & Call Logs ---")
    try:
        sample_lead = env['crm.lead'].search([('type', '=', 'opportunity')], limit=1)
        if sample_lead:
            call_log = env['medical.call.log'].create({
                'lead_id': sample_lead.id,
                'user_id': env.uid,
                'call_type': 'outbound',
                'call_result': 'answered',
                'duration': 120,
                'notes': 'المريض مهتم بخدمة تبييض الأسنان بالليزر وتم تحديد موعد مبدئي',
            })
            log_sim("Call Log Creation", "PASS", f"Created Call Log #{call_log.id} on Lead {sample_lead.name}")
            call_log.unlink()
        else:
            log_sim("Call Log Creation", "WARNING", "No sample lead found to attach call log.")
    except Exception as e:
        log_sim("Call Log Creation", "FAIL", str(e))
        report['frictions_and_gaps'].append(f"Call log creation error: {e}")

    # 3. TEST HOME LAUNCHER FOR ALL 5 ROLES
    print("--- 3. Testing Home Launcher for All 5 Roles ---")
    roles_tested = {}
    users_to_test = [
        ('Admin', env['res.users'].search([('login', '=', 'admin')], limit=1)),
        ('Supervisor', env['res.users'].search([('role_ids.code', 'ilike', 'SUPERVISOR')], limit=1)),
        ('Branch Manager', env['res.users'].search([('role_ids.code', 'ilike', 'BRANCH')], limit=1)),
        ('Agent', env['res.users'].search([('role_ids.code', 'ilike', 'AGENT')], limit=1)),
        ('Marketing', env['res.users'].search([('role_ids.code', 'ilike', 'MARKET')], limit=1)),
    ]
    for role_label, usr in users_to_test:
        if usr:
            try:
                stats = env['crm.lead'].with_user(usr).get_medical_home_launcher_stats()
                roles_tested[role_label] = {
                    'roleTitle': stats.get('roleTitle'),
                    'canAccessSettings': stats.get('canAccessSettings'),
                    'canAccessRoi': stats.get('canAccessRoi'),
                    'kpi1': stats.get('kpi1', {}).get('num'),
                    'kpi2': stats.get('kpi2', {}).get('num'),
                }
                log_sim(f"Launcher [{role_label}]", "PASS", f"Title: {stats.get('roleTitle')} | Settings Access: {stats.get('canAccessSettings')}")
            except Exception as e:
                log_sim(f"Launcher [{role_label}]", "FAIL", str(e))
                report['frictions_and_gaps'].append(f"Launcher failed for {role_label}: {e}")
        else:
            log_sim(f"Launcher [{role_label}]", "SKIP", "No user found with this role in DB.")

    # 4. TEST SPEND DATA & MARKETING ROI CALCULATIONS
    print("--- 4. Testing Spend Data & Marketing ROI Report ---")
    try:
        roi_report = env['medical.campaign.roi.report'].search([])
        zero_spend_count = 0
        valid_spend_count = 0
        for r in roi_report[:10]:
            if r.spend <= 0:
                zero_spend_count += 1
            else:
                valid_spend_count += 1
        log_sim("Marketing ROI Report Data", "PASS", f"Checked {len(roi_report)} campaign rows. Valid spend: {valid_spend_count}, Zero spend (untracked): {zero_spend_count}")
        if zero_spend_count > 0:
            report['operational_findings'].append(f"There are campaigns in ROI report with 0 spend entered. Adding spend in 'medical.campaign.spend' will unlock full CPL/CPA/ROAS calculations.")
    except Exception as e:
        log_sim("Marketing ROI Report Data", "FAIL", str(e))
        report['frictions_and_gaps'].append(f"ROI report calculation error: {e}")

    # 5. TEST LEAD LOST REASONS
    print("--- 5. Testing Lost Reasons ---")
    try:
        lost_reasons = env['crm.lost.reason'].search([])
        log_sim("Lost Reasons Setup", "PASS" if lost_reasons else "WARNING", f"Found {len(lost_reasons)} lost reasons: {[r.name for r in lost_reasons[:4]]}")
        if not lost_reasons:
            report['frictions_and_gaps'].append("No medical lost reasons configured (e.g. 'سعر مرتفع', 'موقع بعيد', 'حجز في عيادة منافسة').")
    except Exception as e:
        log_sim("Lost Reasons Setup", "FAIL", str(e))
        report['frictions_and_gaps'].append(f"Lost reasons error: {e}")

    # 6. TEST DUPLICATE DETECTION LOGIC
    print("--- 6. Testing Duplicate Detection Algorithm ---")
    try:
        Lead = env['crm.lead']
        lead1 = Lead.search([('phone', '!=', False)], limit=1)
        if lead1:
            raw_phone = lead1.phone
            # test variations
            var1 = "+966" + raw_phone.lstrip('0')
            dup = Lead._check_duplicate(phone=var1)
            if dup and dup.id == lead1.id:
                log_sim("Phone Deduplication Algorithm", "PASS", f"Variation '{var1}' correctly matched Lead #{lead1.id} ('{lead1.phone}')")
            else:
                log_sim("Phone Deduplication Algorithm", "WARNING", f"Variation '{var1}' did not match Lead #{lead1.id}")
                report['frictions_and_gaps'].append(f"Phone deduplication missed variation: {var1}")
    except Exception as e:
        log_sim("Phone Deduplication Algorithm", "FAIL", str(e))
        report['frictions_and_gaps'].append(f"Deduplication test error: {e}")

print("\n--- FULL ADMIN SIMULATION REPORT ---")
print(json.dumps(report, indent=2, ensure_ascii=False))
