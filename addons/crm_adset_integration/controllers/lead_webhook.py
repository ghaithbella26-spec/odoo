# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CrmAdsetWebhookController(http.Controller):

    @http.route('/api/v1/crm/lead/webhook', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def receive_lead_webhook(self, **kwargs):
        """ Webhook Endpoint to receive leads from external platforms (Meta, Google, Zapier, custom) """
        
        # 1. Handle Meta (Facebook) Webhook Verification (GET request)
        if request.httprequest.method == 'GET':
            verify_token = kwargs.get('hub.verify_token') or kwargs.get('verify_token')
            challenge = kwargs.get('hub.challenge')
            saved_secret = request.env['ir.config_parameter'].sudo().get_param('crm_adset_integration.webhook_secret')

            if saved_secret and verify_token == saved_secret:
                return challenge or 'OK'
            elif not saved_secret:
                return challenge or 'OK'
            return request.make_response(json.dumps({'status': 'error', 'message': 'Invalid verify token'}), status=403)

        # 2. Handle POST Request (Incoming Lead Data)
        try:
            raw_data = request.httprequest.data
            payload = json.loads(raw_data.decode('utf-8')) if raw_data else kwargs
        except Exception:
            payload = kwargs

        if not payload:
            return request.make_response(
                json.dumps({'status': 'error', 'message': 'Empty payload'}),
                headers=[('Content-Type', 'application/json')],
                status=400
            )

        # 3. Optional Authentication Token Check
        header_token = request.httprequest.headers.get('X-Webhook-Secret') or payload.get('secret_key')
        saved_secret = request.env['ir.config_parameter'].sudo().get_param('crm_adset_integration.webhook_secret')
        if saved_secret and header_token != saved_secret and kwargs.get('verify_token') != saved_secret:
            _logger.warning("CRM Webhook: Rejected request with invalid secret key.")
            return request.make_response(
                json.dumps({'status': 'error', 'message': 'Unauthorized'}),
                headers=[('Content-Type', 'application/json')],
                status=401
            )

        # 4. Extract Lead Fields from Payload
        lead_name = payload.get('name') or payload.get('full_name') or payload.get('contact_name') or 'New Ad Lead'
        email = payload.get('email') or payload.get('email_from')
        phone = payload.get('phone') or payload.get('mobile') or payload.get('phone_number')
        description = payload.get('description') or payload.get('notes') or payload.get('message') or ''
        
        adset_code = payload.get('adset_id') or payload.get('adset_code') or payload.get('utm_content')
        campaign_name = payload.get('utm_campaign') or payload.get('campaign_name')
        source_name = payload.get('utm_source') or payload.get('platform') or 'Social Ads'
        medium_name = payload.get('utm_medium') or 'Paid Ads'

        # 5. Search matching AdSet record
        adset = False
        if adset_code:
            adset = request.env['crm.adset'].sudo().search([('external_id', '=', str(adset_code))], limit=1)
            if not adset:
                adset = request.env['crm.adset'].sudo().search([('name', '=', str(adset_code))], limit=1)

        # Determine Campaign, Source, Medium
        campaign_id = False
        source_id = False
        medium_id = False

        if adset:
            campaign_id = adset.campaign_id.id
            source_id = adset.source_id.id
            medium_id = adset.medium_id.id
        
        if not campaign_id and campaign_name:
            camp = request.env['utm.campaign'].sudo().search([('name', '=', campaign_name)], limit=1)
            if not camp:
                camp = request.env['utm.campaign'].sudo().create({'name': campaign_name})
            campaign_id = camp.id

        if not source_id and source_name:
            src = request.env['utm.source'].sudo().search([('name', '=', source_name)], limit=1)
            if not src:
                src = request.env['utm.source'].sudo().create({'name': source_name})
            source_id = src.id

        if not medium_id and medium_name:
            med = request.env['utm.medium'].sudo().search([('name', '=', medium_name)], limit=1)
            if not med:
                med = request.env['utm.medium'].sudo().create({'name': medium_name})
            medium_id = med.id

        # 6. Prepare Lead Values
        lead_vals = {
            'name': f"{lead_name} - ({adset.name if adset else source_name})",
            'contact_name': lead_name,
            'email_from': email,
            'phone': phone,
            'description': f"Note from Lead: {description}\nReceived via Webhook.",
            'adset_id': adset.id if adset else False,
            'campaign_id': campaign_id,
            'source_id': source_id,
            'medium_id': medium_id,
        }

        if adset:
            if adset.team_id:
                lead_vals['team_id'] = adset.team_id.id
            if adset.user_id:
                lead_vals['user_id'] = adset.user_id.id
            if adset.tag_ids:
                lead_vals['tag_ids'] = [(6, 0, adset.tag_ids.ids)]

        # Create the lead
        new_lead = request.env['crm.lead'].sudo().create(lead_vals)
        _logger.info("Created CRM Lead ID %s via Webhook for AdSet %s", new_lead.id, adset_code)

        return request.make_response(
            json.dumps({'status': 'success', 'lead_id': new_lead.id}),
            headers=[('Content-Type', 'application/json')],
            status=200
        )
