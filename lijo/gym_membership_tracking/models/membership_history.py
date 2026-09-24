from odoo import fields, models

class MembershipHistory(models.Model):
    _name = 'membership.history'
    _description = 'Membership History'

    membership_id = fields.Many2one('res.partner')
    membership_plan = fields.Char(string='Membership Plan')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')