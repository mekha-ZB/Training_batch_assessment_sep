from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RegistrationDetails(models.Model):
    _name = 'registration.details'
    _description = 'registration Details'
    _rec_name = 'attendee_name'
    _inherit=['mail.thread','mail.activity.mixin']

    registration_ref = fields.Char(string='Event Reference',copy=False, readonly=True, default='New')
    event_id = fields.Many2one('event.details',string='EventName',copy=False)
    attendee_name = fields.Many2one('res.partner', string='Attendee Name',copy = False)
    event_date = fields.Date(string='Event Date', related='event_id.date_of_event', store=True)
    event_venue = fields.Many2one('res.partner', string='Event Venue', related='event_id.event_venue', store=True)
    registration_status = fields.Selection([('registered','Registered'),('completed','Completed'),('cancel_request','Cancellation Requested'),('cancelled','Cancelled'),('approved_cancel','Approved Cancellation'),('reject','Rejected Cancellation')], default='registered',copy=False)
    seats_remaining = fields.Integer(string='Seats Remaining',compute='_compute_seats_remaining')
    is_event_coordinator = fields.Boolean(string= 'Is Event Coordinator',default=False)
    is_senior_coordinator = fields.Boolean(string= 'Is Senior Coordinator',default=False)
    
    
    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            if record.get('registration_ref', 'New') == 'New':
                record['registration_ref'] = self.env['ir.sequence'].next_by_code('registration.seq') or 'New'
        return super().create(vals)

    def send_mail(self):
            self.ensure_one()
            
            ctx = {
                'default_model': 'registration.details',
                'default_res_ids': self.ids,
                'default_composition_mode': 'comment',
                'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
                'email_notification_allow_footer': True,
                'hide_mail_template_management_options': True,
                'default_partner_ids': self.attendee_name.ids,
                'default_reply_to': self.attendee_name.email,
                'force_email': True,
            }
            self.registration_status='completed'
            if not self.env.context.get('hide_default_template'):
                mail_template = self.env.ref(
                    'event_management.registration_confirmation_email',
                    raise_if_not_found=False,
                )
    
                if mail_template:
                    ctx.update({
                        'default_template_id': mail_template.id,
                    })
            
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Compose Email',
                'res_model': 'mail.compose.message',
                'view_mode': 'form',
                'target': 'new',
                'context': ctx,
                
            }
            
        
    @api.depends('event_id')
    def _compute_seats_remaining(self):
        total_seat_capacity = self.event_venue.seat_capacity
        reamining_seats = self.env['registration.details'].search_count([('event_id', '=', self.event_id.id)])
        for record in self:
            if record.registration_status in ['registered','completed','cancel_request']:
                record.seats_remaining = total_seat_capacity - reamining_seats
            else:
                record.seats_remaining = 0

    def request_cancel(self):
        self.registration_status = 'cancel_request'
            
    def approve_cancel(self):
        self.registration_status = 'approved_cancel'
            
    def reject_cancel(self):
        self.registration_status = 'reject'
        
    def cancel_button(self):
            self.registration_status = 'cancelled'
        
    @api.constrains('attendee_name','event_id')
    def registration_ensure(self):
        for rec in self:
            if rec.attendee_name and rec.event_id:
                attendees= self.search_count([('attendee_name','=',rec.attendee_name.id),('event_id','=',rec.event_id.id),('id','!=',rec.id)])
                if attendees>=1:
                    raise ValidationError("You are Already Registered for this Event.")
                
    @api.constrains('seats_remaining')
    def seats_ensure(self):
        if self.seats_remaining <= 0:
            raise ValidationError("No Seats Available!")