from odoo import fields,api,models
from odoo.exceptions import ValidationError,UserError

class MovieBooking(models.Model):
    _name = 'movie.booking'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Booking details'
    _rec_name = 'booking_sequence'
    
    customer_id = fields.Many2one('res.partner',string='Customer Name')
    show_id = fields.Many2one('movie.movies', string='Show')
    hall_id = fields.Many2one('movie.halls',string='Hall')
    total_seats_available = fields.Many2many('movie.seats','available_seats',string='Available Seats',compute="_total_seats_available_in_Audi")
    number_of_seats = fields.Many2many('movie.seats',string='Seats')
    seat_remaining = fields.Integer(string='Seat Remaining',compute="compute_seat_remaining")
    booking_sequence = fields.Char(string='Booking ID', default='New')
    status = fields.Selection([
        ('booked','Booked'),
        ('completed','Completed'),
        ('cancellation_request','Cancellation Request'),
        ('cancelled','Cancelled'),
        ], default='booked')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('booking_sequence', 'New') == 'New':
                vals['booking_sequence'] = self.env['ir.sequence'].next_by_code('movie.booking') or 'New'
        return super().create(vals_list)
    
    @api.depends('total_seats_available')
    def compute_seat_remaining(self):
        for rec in self:
            # if not rec.total_seats_available:
            #     rec.seat_remaining = False
            #     continue
            
            rec.seat_remaining = len(rec.total_seats_available)
            
    # def seat_available_smart_button(self):
    #     for rec in self:
    #         pass
    
    def seat_available_smart_button(self):
        self.ensure_one()
        # print("123=================>",self.total_seats_available.ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seats records',
            'res_model': 'movie.seats',
            'view_mode': 'list,form',
            'domain': [('id', '=', self.total_seats_available.ids)],
            # 'context': {'default_seats_id': self.ids},
        }

    
    @api.depends('hall_id','show_id','status')
    def _total_seats_available_in_Audi(self):
        for rec in self:
            
            if rec.hall_id:
                booked_seats = self.search([
                    ('hall_id', '=', rec.hall_id.id),
                    ('show_id', '=', rec.show_id.id),
                    ('status','in',['booked','completed','cancellation_request']),
                    # ('status','=','completed'),
                    # ('status','=','cancellation_request'),
                    # ('status','=','cancelled'),
                    ]).mapped('number_of_seats')
                rec.total_seats_available = rec.hall_id.hall_seats_ids - booked_seats
                print('total_seats---',rec.total_seats_available)
            else:
                rec.total_seats_available = False
    
    
    def action_confirm(self):
            self.status = 'completed'
    def action_cancel_request(self):
            self.status = 'cancellation_request'
    def action_to_cancelled(self):
            self.status = 'cancelled'
    def action_reset_to_booked(self):
            self.status = 'booked'

    def action_send_email(self):
            self.ensure_one()
            ctx = {
                'default_model': 'movie.booking',
                'default_res_ids': self.ids,
                'default_composition_mode': 'comment',
                'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
                'email_notification_allow_footer': True,
                'hide_mail_template_management_options': True,
                'default_partner_ids': self.customer_id.ids,
                'default_reply_to': self.customer_id.email,
                'force_email': True,
            }
    
            if not self.env.context.get('hide_default_template'):
                mail_template = self.env.ref(
                    'movie_ticket_booking.mail_template_booking_details',
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
            
    # @api.depends('hall_id','show_id','status')
        # def _total_seats_available_in_Audi(self):
        #     for rec in self:
        #         if rec.hall_id:
                    # print('yes--------------------')
                    # print(rec.hall_id.hall_seats_ids)
                    # booked_seats = self.search([('status','=','booked')]).mapped('number_of_seats')
                    # print('booked_seats ----',booked_seats)
                    # total_seats =  set(rec.hall_id.hall_seats_ids.ids) - set(booked_seats.ids)
                    # print('total_seats---',total_seats)
                    
                    # rec.write({'total_seats_available': [(6,0,list(total_seats))]})
                # else:
                    # rec.total_seats_available = False        
            
                       
   
                
                
                
                
                
    # @api.depends('hall_id', 'show_id', 'status')
    # def _total_seats_available_in_Audi(self):
    #     for rec in self:
    #         if not rec.hall_id:
    #             rec.total_seats_available = False
    #             continue

    #         booked_seats = self.search([
    #             ('hall_id', '=', rec.hall_id.id),
    #             ('show_id', '=', rec.show_id.id),
    #             ('status', '=', 'booked'),
    #         ]).mapped('number_of_seats')

    #         rec.total_seats_available = rec.hall_id.hall_seats_ids - booked_seats
            