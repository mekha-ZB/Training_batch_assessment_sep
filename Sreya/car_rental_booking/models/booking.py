from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BookingDetails(models.Model):
    _name = 'booking.details'
    _description = 'Booking Details'
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name = 'customer_id'
    
    customer_id = fields.Many2one('res.partner', string="Customer Name")
    model = fields.Many2one('vehicle.details',string="Model")
    pick_up_date = fields.Date(string="PickUp Date")
    return_date = fields.Date(string="Return Date")
    state = fields.Selection([('draft' , 'Draft'),('confirmed' , 'Confirmed'), ('returned', 'Returned'), ('cancelled', 'Request For Cancellation'),('approve','Approved Cancellation'),('reject','Rejected Cancelation'),('cancel','Cancelled Booking')],default='draft')
    seq = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    daily_rate = fields.Float(string="Daily Rate")
    rental_days = fields.Integer(string='Rental Days',compute='_compute_rental_days',store=True)
    total_cost = fields.Float(string="Total Rental Cost", compute="_compute_total_cost",store=True)
    
    @api.depends('pick_up_date', 'return_date')
    def _compute_rental_days(self):
        for record in self:
            if record.pick_up_date and record.return_date:
                record.rental_days=(record.return_date - record.pick_up_date).days+1
            else:
                record.rental_days=0
                
    @api.depends('rental_days', 'daily_rate')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.rental_days*record.daily_rate
    
    @api.onchange('model')
    def onchange_model_type(self):
        if self.model:
            self.daily_rate = self.model.daily_rate
        else:
            self.daily_rate = False
            
    @api.constrains('model', 'pick_up_date', 'return_date')
    def _check_vehicle(self):
        for record in self:
            if not record.model or not record.pick_up_date or not record.return_date:
                continue
            domain = [
                ('id', '!=', record.id),
                ('model', '=', record.model.id),
                ('state', '=', 'confirmed'),
                ('pick_up_date', '<=', record.return_date),
                ('return_date', '>=', record.pick_up_date),
            ]
            if self.search_count(domain):
                raise ValidationError('This car is already booked for these dates.')
        
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('seq','New') == 'New':
                val['seq'] = self.env['ir.sequence'].next_by_code('booking.id') or 'New'
        return super(BookingDetails, self).create(vals_list)
    
    def confirm_button(self):
        self.state = 'confirmed'
        
    def return_button(self):
        self.state = 'returned'
        
    def cancel_request_button(self):
        self.state = 'cancelled'
        
    def approve_button(self):
        self.state = 'approve'
        
    def reject_button(self):
        self.state = 'reject'
        
    def cancel_button(self):
        self.state = 'cancel'
        
    def send_email(self):
            self.ensure_one()
            ctx = {
                'default_model': 'booking.details',
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
                    'car_rental_booking.booking_confirmation_email',
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
    
    
    # def cancel_request_button(self):
    #     return {
    #         # open pop up
    #         'type': 'ir.actions.act_window',
    #         'name': 'Reason For Cancellation',
    #         'res_model': 'booking.wizard',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {'active_ids': self.ids},
    #     }