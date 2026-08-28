# -*- coding: utf-8 -*-
import secrets
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    crm_webhook_secret = fields.Char(
        string='Webhook Secret Key',
        config_parameter='crm_adset_integration.webhook_secret',
        default=lambda self: self._default_webhook_secret(),
        help='Secret key used to authenticate incoming webhook requests'
    )
    crm_webhook_url = fields.Char(
        string='Webhook Receiver URL',
        compute='_compute_crm_webhook_url',
        default=lambda self: self._get_webhook_url(),
        help='URL to set up in Facebook / Google / Zapier for sending leads'
    )

    def _default_webhook_secret(self):
        secret = self.env['ir.config_parameter'].sudo().get_param('crm_adset_integration.webhook_secret')
        if not secret:
            secret = secrets.token_hex(16)
            self.env['ir.config_parameter'].sudo().set_param('crm_adset_integration.webhook_secret', secret)
        return secret

    def _get_webhook_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') or 'http://localhost:8069'
        return f"{base_url.rstrip('/')}/api/v1/crm/lead/webhook"

    @api.depends('crm_webhook_secret')
    def _compute_crm_webhook_url(self):
        url = self._get_webhook_url()
        for record in self:
            record.crm_webhook_url = url

    def action_generate_webhook_secret(self):
        secret = secrets.token_hex(16)
        self.env['ir.config_parameter'].sudo().set_param('crm_adset_integration.webhook_secret', secret)
        self.crm_webhook_secret = secret
        self.crm_webhook_url = self._get_webhook_url()
