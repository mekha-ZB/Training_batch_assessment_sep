from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    booking_ids = fields.One2many('hotel.booking','customer_id', string='Hotel Bookings')
    total_stays = fields.Integer(string='Total Stays',compute='_compute_total_stays',store=True)

    @api.depends('booking_ids.status')
    def _compute_total_stays(self):
        for partner in self:
            partner.total_stays = len(partner.booking_ids.filtered(lambda booking: booking.status != 'cancelled'))

    def action_view_bookings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hotel Bookings',
            'res_model': 'hotel.booking',
            'view_mode': 'list,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {
                'default_customer_id': self.id,
            },
        }