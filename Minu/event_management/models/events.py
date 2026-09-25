from odoo import models, fields, api

class EventDetails(models.Model):
    _name = 'event.details'
    _description = 'Event Details'
    _rec_name = 'event_name'
    _inherit=['mail.thread','mail.activity.mixin']

    event_ref = fields.Char(string='Event Reference',copy=False, readonly=True, default='New')
    event_name = fields.Char(string='Event Name',copy = False)
    date_of_event =fields.Date(string="Date",copy=False)
    event_venue = fields.Many2one('res.partner', string='Event Venue',copy = False)
    capacity = fields.Integer(string='Capacity',copy = False ,related='event_venue.seat_capacity')

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            if record.get('event_ref', 'New') == 'New':
                record['event_ref'] = self.env['ir.sequence'].next_by_code('event.seq') or 'New'
        return super().create(vals)

   
        