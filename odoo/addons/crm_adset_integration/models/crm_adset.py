# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CrmAdset(models.Model):
    _name = 'crm.adset'
    _description = 'Advertising Ad Set'
    _order = 'name, id desc'

    name = fields.Char(string='Ad Set Name', required=True, tracking=True)
    external_id = fields.Char(string='Platform AdSet ID', required=True, index=True,
                              help='External ID or Code from Ad Platform (e.g. Meta AdSet ID)')
    platform = fields.Selection([
        ('facebook', 'Meta (Facebook / Instagram)'),
        ('google', 'Google Ads'),
        ('tiktok', 'TikTok Ads'),
        ('snapchat', 'Snapchat Ads'),
        ('custom', 'Custom / Other'),
    ], string='Ad Platform', default='facebook', required=True)

    campaign_id = fields.Many2one('utm.campaign', string='UTM Campaign', ondelete='set null')
    source_id = fields.Many2one('utm.source', string='UTM Source', ondelete='set null')
    medium_id = fields.Many2one('utm.medium', string='UTM Medium', ondelete='set null')

    team_id = fields.Many2one('crm.team', string='Assigned Sales Team',
                              help='Sales team to assign incoming leads from this AdSet')
    user_id = fields.Many2one('res.users', string='Assigned Salesperson',
                             help='Default salesperson assigned to incoming leads')
    tag_ids = fields.Many2many('crm.tag', string='Default Tags',
                               help='Tags to automatically apply to incoming leads')

    active = fields.Boolean(default=True)
    lead_ids = fields.One2many('crm.lead', 'adset_id', string='Leads')
    lead_count = fields.Integer(string='Leads Count', compute='_compute_lead_count')

    @api.depends('lead_ids')
    def _compute_lead_count(self):
        for record in self:
            record.lead_count = len(record.lead_ids)

    def action_view_leads(self):
        self.ensure_one()
        return {
            'name': 'Leads',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain': [('adset_id', '=', self.id)],
            'context': {'default_adset_id': self.id},
        }
