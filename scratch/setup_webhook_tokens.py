import sys
import secrets

sys.path.insert(0, r'd:\Odoo\odoo')
import odoo
from odoo import api, SUPERUSER_ID

config = odoo.tools.config
config.parse_config(['-c', 'd:\\Odoo\\odoo\\odoo.conf', '-d', 'dbodoo18'])

registry = odoo.registry('dbodoo18')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    # 1. Set global webhook token in ir.config_parameter
    global_token = f"gsk_sec_{secrets.token_hex(16)}"
    env['ir.config_parameter'].set_param('medical_crm_api.webhook_token', global_token)
    print(f"Generated global Webhook Secret Token: {global_token}")

    # 2. Setup/Verify medical.api.config for all 4 platforms
    platforms = env['medical.platform'].search([])
    for p in platforms:
        cfg = env['medical.api.config'].search([('platform_id', '=', p.id)], limit=1)
        if not cfg:
            cfg = env['medical.api.config'].create({
                'name': f'ربط إعلانات {p.name}',
                'platform_id': p.id,
                'sync_status': 'connected',
                'webhook_token': f"gsk_{p.code}_{secrets.token_hex(12)}"
            })
            print(f"Created API Config for {p.name} with URL: {cfg.webhook_url} and Token: {cfg.webhook_token}")
        else:
            if not cfg.webhook_token:
                cfg.webhook_token = f"gsk_{p.code}_{secrets.token_hex(12)}"
            cfg.sync_status = 'connected'
            print(f"Verified API Config for {p.name} with URL: {cfg.webhook_url} and Token: {cfg.webhook_token}")

    cr.commit()
    print("SUCCESS: Webhook Security Tokens generated and configured.")
