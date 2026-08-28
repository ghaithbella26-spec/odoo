import sys
import os
import json
import traceback

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')

results = {
    'summary': {},
    'tests': [],
    'errors_found': [],
    'frictions_found': [],
    'warnings': []
}

def log_test(name, status, details=""):
    results['tests'].append({'name': name, 'status': status, 'details': details})

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # TEST 1: Check SQL Views in medical_crm_reports
    print("--- 1. Testing SQL OLAP Reports Views ---")
    report_models = [
        'medical.campaign.roi.report',
        'medical.crm.report',
        'medical.agent.report',
        'medical.funnel.report'
    ]
    for model_name in report_models:
        try:
            if model_name in env:
                records = env[model_name].search([], limit=5)
                fields_data = env[model_name].fields_get()
                log_test(f"Report Model [{model_name}]", "PASS", f"Found {len(records)} sample records, {len(fields_data)} fields defined.")
            else:
                log_test(f"Report Model [{model_name}]", "FAIL", "Model not registered in registry.")
                results['errors_found'].append(f"Model {model_name} missing from registry.")
        except Exception as e:
            log_test(f"Report Model [{model_name}]", "FAIL", str(e))
            results['errors_found'].append(f"Error querying {model_name}: {e}")

    # TEST 2: Check Webhook API & Logging
    print("--- 2. Testing Webhook Logging & Config ---")
    try:
        api_log_count = env['medical.api.log'].search_count([]) if 'medical.api.log' in env else 0
        webhook_token = env['ir.config_parameter'].get_param('medical_crm_api.webhook_token')
        log_test("Webhook Config & Logs", "PASS" if webhook_token else "WARNING", f"Token: {webhook_token}, Logs Count: {api_log_count}")
        if not webhook_token:
            results['warnings'].append("Webhook token 'medical_crm_api.webhook_token' is not set in ir.config_parameter.")
    except Exception as e:
        log_test("Webhook Config & Logs", "FAIL", str(e))
        results['errors_found'].append(f"Webhook test error: {e}")

    # TEST 3: Check Roles & User Permissions
    print("--- 3. Testing Roles & User Setup ---")
    try:
        roles = env['res.users.role'].search([])
        users_without_role = env['res.users'].search([('role_ids', '=', False), ('id', '!=', 1)])
        log_test("User Roles Check", "PASS", f"Total Roles: {len(roles)}, Users without Role: {len(users_without_role)}")
        if users_without_role:
            results['warnings'].append(f"{len(users_without_role)} users have no role assigned (e.g., {[u.login for u in users_without_role[:3]]}).")
    except Exception as e:
        log_test("User Roles Check", "FAIL", str(e))
        results['errors_found'].append(f"Roles test error: {e}")

    # TEST 4: Check Branches & Multi-Company Structure
    print("--- 4. Testing Multi-Company Branches ---")
    try:
        parent_comp = env['res.company'].search([('parent_id', '=', False), ('id', '!=', 1)], limit=1)
        branches = env['res.company'].search([('parent_id', '!=', False)])
        leads_without_branch = env['crm.lead'].search_count([('branch_id', '=', False)])
        leads_without_clinic = env['crm.lead'].search_count([('clinic_id', '=', False)])
        log_test("Branch Structure Check", "PASS", f"Main: {parent_comp.name if parent_comp else 'None'}, Branches: {len(branches)}, Leads w/o branch: {leads_without_branch}, Leads w/o clinic: {leads_without_clinic}")
        if leads_without_branch > 0:
            results['frictions_found'].append(f"There are {leads_without_branch} leads with no branch_id set, which means branch managers cannot see them.")
        if leads_without_clinic > 0:
            results['frictions_found'].append(f"There are {leads_without_clinic} leads with no clinic_id (specialty) set.")
    except Exception as e:
        log_test("Branch Structure Check", "FAIL", str(e))
        results['errors_found'].append(f"Branch test error: {e}")

    # TEST 5: Check Distribution Rules
    print("--- 5. Testing Lead Distribution Engine ---")
    try:
        rules = env['medical.distribution.rule'].search([])
        log_test("Distribution Rules", "PASS" if rules else "WARNING", f"Configured Rules: {len(rules)}")
        if not rules:
            results['frictions_found'].append("No auto-distribution rules currently active in medical.distribution.rule; newly imported leads might remain unassigned if not targeted.")
    except Exception as e:
        log_test("Distribution Rules", "FAIL", str(e))
        results['errors_found'].append(f"Distribution rules test error: {e}")

    # TEST 6: Check SLA Hours & Stage Configuration
    print("--- 6. Testing SLA Stage Setup ---")
    try:
        stages = env['crm.stage'].search([])
        stages_without_sla = stages.filtered(lambda s: not s.sla_hours or s.sla_hours <= 0)
        log_test("Stage SLA Setup", "PASS", f"Total Stages: {len(stages)}, Stages w/o SLA: {len(stages_without_sla)}")
        if stages_without_sla:
            results['frictions_found'].append(f"Stages without SLA hours defined: {[s.name for s in stages_without_sla]}.")
    except Exception as e:
        log_test("Stage SLA Setup", "FAIL", str(e))
        results['errors_found'].append(f"SLA stage test error: {e}")

    # TEST 7: Check Home Launcher RPC
    print("--- 7. Testing Home Launcher RPC ---")
    try:
        stats = env['crm.lead'].get_medical_home_launcher_stats()
        log_test("Launcher RPC Method", "PASS", f"Returned role: {stats.get('roleTitle')}, kpi1: {stats.get('kpi1', {}).get('num')}")
    except Exception as e:
        log_test("Launcher RPC Method", "FAIL", str(e))
        results['errors_found'].append(f"Home launcher RPC failed: {e}")

    # TEST 8: Check Menu & Window Action Integrities
    print("--- 8. Testing Menus and Actions ---")
    try:
        broken_menus = []
        menus = env['ir.ui.menu'].search([('action', '!=', False)])
        for m in menus:
            action_ref = m.action
            if not action_ref:
                broken_menus.append(m.name)
        log_test("Menu Action Integrity", "PASS" if not broken_menus else "FAIL", f"Tested {len(menus)} action menus. Broken: {len(broken_menus)}")
    except Exception as e:
        log_test("Menu Action Integrity", "FAIL", str(e))
        results['errors_found'].append(f"Menu action integrity test error: {e}")

print("\n--- DIAGNOSTIC RESULTS ---")
print(json.dumps(results, indent=2, ensure_ascii=False))
