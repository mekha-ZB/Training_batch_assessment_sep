from odoo import models, fields

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    total_active_membership = fields.Integer(string='Active Membership', compute='_compute_count_of_active_membership')
    membership_history_ids = fields.One2many(comodel_name='membership.history', inverse_name='membership_id', string='History')

    def _compute_count_of_active_membership(self):
        active_count = self.env['membership.details'].search_count(['&',('status', '=', 'active'),('member_id', '=', self.id)])
        self.total_active_membership = active_count
        return self.total_active_membership


    def action_open_active_membership(self):
        if self.total_active_membership:
            return {
                'name': 'Active Membership',
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'membership.details',
                'domain': ['&',('status', '=', 'active'),('member_id', '=', self.id)]
            }
        return None
