import base64
from odoo import fields, models, api
from odoo.exceptions import ValidationError,UserError

class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Hotel Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Booking Reference',required=True,copy=False,readonly=True,default='New')
    customer_number = fields.Char(string='Sequence Number', required=True, copy=False, readonly=True, default='New', )
    customer_id = fields.Many2one('res.partner',string = 'Customer',required = True)
    room_id = fields.Many2one('hotel.room',string = 'Room',required = True)
    check_in = fields.Date(string='Check-in Date', required=True)
    check_out = fields.Date(string='Check-out Date', required=True)
    rate_per_night = fields.Float(string = 'Rate Per Night',required = True)
    number_of_nights = fields.Integer(string = 'Number of Nights',compute = '_compute_booking_amount',store = True)
    total_price = fields.Float(string = 'Total Price',compute = '_compute_booking_amount',store = True)
    status = fields.Selection([('confirmed', 'Confirmed'),('cancellation_requested', 'Cancellation Requested'),('cancelled', 'Cancelled'),('checked_out', 'Checked Out')], string='Status', default='confirmed', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('customer_number', 'New') == 'New':
                vals['customer_number'] = self.env['ir.sequence'].next_by_code('hotel.booking') or 'New'
        return super().create(vals_list)

    @api.constrains('check_in', 'check_out')
    def _check_booking_dates(self):
        for record in self:
            if (record.check_in and record.check_out and
                    record.check_out <= record.check_in):
                raise ValidationError("Invalid Date")

    @api.depends('check_in', 'check_out', 'rate_per_night')
    def _compute_booking_amount(self):
        for booking in self:
            if booking.check_in and booking.check_out:
                booking.number_of_nights = (booking.check_out - booking.check_in).days
            else:
                booking.number_of_nights = 0
            booking.total_price = booking.number_of_nights * booking.rate_per_night

    @api.onchange('room_id')
    def _onchange_room_id(self):
        if self.room_id:
            self.rate_per_night = self.room_id.rate_per_night


    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref('hotel_booking_management.mail_template_hotel_booking_confirmation')
        report = self.env.ref('hotel_booking_management.action_report_hotel_booking')
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report,res_ids=self.ids,)
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.customer_id.name} - Booking Confirmation.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'hotel.booking',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Email',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'hotel.booking',
                'default_res_ids': self.ids,
                'default_template_id': template.id,
                'default_attachment_ids': [attachment.id],
                'force_email': True,

            },
        }

    def action_request_cancellation(self):
        if not self.env.user.has_group('hotel_booking_management.group_staff_users'):
            raise UserError('Only Front Desk Staff can request a cancellation')
        if self.status != 'confirmed':
            raise UserError('Only confirmed bookings can request cancellation')
        self.status = 'cancellation_requested'

    def action_approve_cancellation(self):
        if not (self.env.user.has_group('hotel_booking_management.group_supervisor_users')
                or self.env.user.has_group('hotel_booking_management.group_manager_user')):
            raise UserError('Only Supervisor/Manager can approve cancellation')
        if self.status != 'cancellation_requested':
            raise UserError('Only cancellation requests can be approved')
        self.status = 'cancelled'

    def action_reject_cancellation(self):
        if not (self.env.user.has_group('hotel_booking_management.group_supervisor_users')
                or self.env.user.has_group('hotel_booking_management.group_manager_user')):
            raise UserError('Only Supervisor/Manager can reject cancellation')
        if self.status != 'cancellation_requested':
            raise UserError('Only cancellation requests can be rejected')
        self.status = 'confirmed'

    def action_check_out(self):
        if self.status != 'confirmed':
            raise UserError('Only confirmed bookings can be checked out')
        self.status = 'checked_out'



