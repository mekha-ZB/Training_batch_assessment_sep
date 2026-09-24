from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import date


class MemberDetails(models.Model):
    _name = 'membership.details'
    _description = 'Gym Member Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'member_id'

    seq_num = fields.Char(string='Sequence', default='New', copy=False, required=True)
    member_id = fields.Many2one(comodel_name='res.partner', string='Member')

    phone = fields.Char(string='Phone')
    age = fields.Integer(string='Age')
    email = fields.Char(string='Email')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')

    plan_id = fields.Many2one(comodel_name='membership.plan', string='Plan')
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    end_date = fields.Date(string='End Date')
    membership_fee = fields.Float(string='Membership Fee')

    status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancellation_requested', 'Cancellation Requested'),
        ('cancelled', 'Cancelled'),
    ], string='Status',default='active')

    cancellation_request = fields.Text(string='Note')

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            if rec.get('seq_num', 'New') == 'New':
                rec['seq_num'] = self.env['ir.sequence'].next_by_code('membership.details.code') or 'New'
        return super().create(vals_list)


    def submit_cancellation_request(self):
        if self.cancellation_request:
            self.status = 'cancellation_requested'
        else:
            raise ValidationError("Enter a cancellation request")


    @api.onchange('plan_id', 'start_date', 'member_id')
    def onchange_end_date(self):
        for rec in self:
            if rec.member_id:
                rec.phone = rec.member_id.phone
                rec.email = rec.member_id.email
            if rec.plan_id and not rec.start_date:
                rec.start_date = fields.Date.today()
            if rec.plan_id and rec.start_date:
                rec.end_date = (rec.start_date + relativedelta(
                    months=rec.plan_id.duration_months) - relativedelta(days=1))
            else:
                rec.end_date = False


    @api.model
    def check_expired_records(self):
        today = date.today()
        record_expire = self.search([('status', '=', 'active'), ('end_date', '<', today)])
        record_expire.write({'status': 'expired'})

        record_active = self.search([('status', '=', 'active'),('end_date', '>', today)])
        record_active.write({'status': 'active'})


    def send_mail(self):
        template = self.env.ref('gym_membership_tracking.mail_template_membership_details', raise_if_not_found=False)

        if not template:
            raise UserError("Mail Template not found. Please check the template.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Email',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': self._name,
                'default_res_ids': [self.id],
                'default_template_id': template.id,
                'default_reply_to': self.env.user.email,
                'default_composition_mode': 'comment',
            },
        }


    def approve_cancellation_request(self):
        self.status = 'cancelled'

    def reject_cancellation_request(self):
        self.status = 'active'


    def unlink(self):
        for record in self:
            if record.status == 'expired':
                if not self.env.user.has_group(
                        'gym_membership_tracking.group_gym_manager'
                ):
                    raise UserError(
                        'Only the Gym Manager can delete an expired membership.'
                    )
        return super().unlink()


    def write(self, vals):
        if 'plan_id' in vals or 'start_date' in vals or 'end_date' in vals:
            if self.plan_id and self.start_date and self.end_date:
                self.env['membership.history'].create({
                    'membership_id': self.member_id.id,
                    'membership_plan': self.plan_id.plan_name,
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                })
        return super().write(vals)
