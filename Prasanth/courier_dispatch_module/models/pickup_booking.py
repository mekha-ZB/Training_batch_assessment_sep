from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PickupBooking(models.Model):
    _name = 'pickup.booking'
    _description = 'Pickup Booking'
    _rec_name='booking_seq'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    booking_seq=fields.Char(string='Booking Sequence', required=True,copy=False, readonly=True, default=lambda self: _('New'))
    product_line_ids=fields.One2many('product.line.id','pickup_id',string='Products')
    customer_id=fields.Many2one('res.partner',string='Customer Name',copy=False)
    company_id=fields.Many2one('res.company',string='Company Name',copy=False)
    courier_id=fields.Many2one('res.partner',string='Courier Incharge', tracking=True,copy=False)

    pickup_street = fields.Char(string='Address', store=True,copy=False)
    pickup_city = fields.Char(string='City', store=True,copy=False)
    pickup_state_id = fields.Many2one('res.country.state', string='State',copy=False)
    pickup_country_id = fields.Many2one('res.country', string='Country',copy=False)
    pickup_zip = fields.Char(string='Zip',copy=False)


    delivery_street = fields.Char(string='Delivery Address',copy=False)
    delivery_city = fields.Char(string='Delivery City',copy=False)
    delivery_state_id = fields.Many2one('res.country.state', string='Delivery State',copy=False)
    delivery_country_id = fields.Many2one('res.country', string='Delivery Country',copy=False)
    delivery_zip = fields.Char(string='Delivery Zip',copy=False)
   

    delivery_date=fields.Date(string='Delivery Date',tracking=True,copy=False)
    booking_date=fields.Date(string='Booking Date',tracking=True,copy=False)

    cust_phone=fields.Char(string='Phone',copy=False)
    cust_email=fields.Char(string='Email',copy=False)

    booking_status=fields.Selection([('scheduled','Scheduled'),('delivered','Delivered'),('cancellation_requested','Cancellation Requested'),('cancelled','Cancelled')],string='Booking Status',default='scheduled',tracking=True)

    @api.constrains('booking_date','delivery_date')
    def _constrains_dates(self):
        for rec in self:
            if rec.booking_date > rec.delivery_date:
                raise ValidationError(_('Booking Date cannot be greater than Delivery Date'))

    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('booking_seq', 'New') == 'New':
                vals['booking_seq'] = self.env['ir.sequence'].next_by_code('pickup.booking.sequence') or 'New'
        return super(PickupBooking, self).create(vals_list)

    @api.constrains('product_line_ids')
    def _constrains_product_line_ids(self):
        for rec in self:
            if not rec.product_line_ids:
                raise ValidationError(_('Product Line cannot be empty'))


    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            self.pickup_street = self.company_id.street
            self.pickup_city = self.company_id.city
            self.pickup_state_id = self.company_id.state_id
            self.pickup_country_id = self.company_id.country_id
            self.pickup_zip = self.company_id.zip

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        if self.customer_id:
            self.delivery_street = self.customer_id.street
            self.delivery_city = self.customer_id.city
            self.delivery_state_id = self.customer_id.state_id
            self.delivery_country_id = self.customer_id.country_id
            self.delivery_zip = self.customer_id.zip
            self.cust_phone=self.customer_id.phone
            self.cust_email=self.customer_id.email

    
    def action_scheduled(self):
        for rec in self:
            rec.booking_status = 'scheduled'

    def action_delivered(self):
        for rec in self:
            rec.booking_status = 'delivered'

    def action_cancellation_requested(self):
        for rec in self:
            rec.booking_status = 'cancellation_requested'

    def action_cancelled(self):
        for rec in self:
            rec.booking_status = 'cancelled'

    def action_button_print(self):
        self.ensure_one()
        return self.env.ref('courier_dispatch_module.action_courier_report').report_action(self)

    def action_send_mail(self):

        ctx = {
            'default_model': 'pickup.booking',
            'default_res_ids': self.ids,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'email_notification_allow_footer': True,
            'hide_mail_template_management_options': True,
            'default_reply_to': self.company_id.email or self.env.company.email,
            'default_email_from': self.company_id.email or self.env.company.email or self.env.user.email_formatted,
            'default_partner_ids':self.customer_id.ids,

        }

        if len(self) > 1:
            ctx['default_composition_mode'] = 'mass_mail'
        else:
            ctx.update({
                'force_email': True,
            })
            if not self.env.context.get('hide_default_template'):
                mail_template = self.env.ref('courier_dispatch_module.mail_template_courier_details', raise_if_not_found=False)
                if mail_template:
                    ctx.update({
                        'default_template_id': mail_template.id,
                        'mark_so_as_sent': True,
                    })
            else:
                pass
        
        action = {
            'name': ('Send'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
       
        return action

    def action_view_all_bookings(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard'),
            'res_model': 'wizard.booking',
            'view_mode': 'form',
            'target': 'new',
        }
        
    