from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date


class MembershipRenewalWizard(models.TransientModel):
    _name = 'membership.renewal.wizard'
    _description = 'Membership Renewal Wizard'

    plan_id = fields.Many2one('membership.plan',string='Renewal Plan')
    start_date = fields.Date(string='Start Date',default=fields.Date.context_today)
    end_date = fields.Date(string='End Date')
    membership_fee = fields.Float(string='Membership Fee')

    @api.onchange('plan_id', 'start_date')
    def onchange_end_date(self):
        for rec in self:
            if rec.plan_id and not rec.start_date:
                rec.start_date = fields.Date.today()

            if rec.plan_id and rec.start_date:
                rec.end_date = (rec.start_date + relativedelta(
                    months=rec.plan_id.duration_months) - relativedelta(days=1))
                rec.membership_fee = rec.plan_id.membership_fee


    def action_renew_membership(self):
        self.ensure_one()
        membership_id = self.env.context.get('active_id')
        membership = self.env['membership.details'].browse(membership_id)

        membership.write({
            'plan_id': self.plan_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'membership_fee': self.membership_fee,
            'status': 'active',
        })

        return {'type': 'ir.actions.act_window_close'}