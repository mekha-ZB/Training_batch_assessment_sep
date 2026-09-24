from odoo import models, fields

class GymMembershipPlan(models.Model):
    _name = 'membership.plan'
    _description = 'Gym Membership Plan'
    _rec_name = 'plan_name'

    plan_name = fields.Char(string='Plan Name', copy=False)
    duration_months = fields.Integer(string='Duration Months')
    membership_fee = fields.Float(string='Membership Fee')