from odoo import fields, models, api

class HotelCustomer(models.Model):
    _name = 'hotel.customers'
    _description = 'Hotel Customer'

    partner_id = fields.Many2one('res.partner',string='Customer',required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')
    booking_ids = fields.One2many('hotel.booking','customer_id',string='Hotel Bookings')
    total_stays = fields.Integer(string='Total Stays',compute='_compute_total_stays',store=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.email = self.partner_id.email
            self.address = self.partner_id.contact_address


    @api.depends('booking_ids.status')
    def _compute_total_stays(self):
        for customer in self:
            customer.total_stays = len(customer.booking_ids.filtered(lambda booking: booking.status != 'cancelled') )

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