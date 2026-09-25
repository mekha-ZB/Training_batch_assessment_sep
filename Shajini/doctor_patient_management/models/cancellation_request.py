from odoo import fields, models


class AppointmentCancellationRequest(models.Model):
    _name = 'appointment.cancellation.request'
    _description = 'Appointment Cancellation Request'
    _order = 'request_date desc'

    appointment_id = fields.Many2one('appointment',string='Appointment',required=True)
    requested_by = fields.Many2one('res.users',string='Requested By',default=lambda self: self.env.user,readonly=True)
    reason = fields.Text(string='Cancellation Reason',required=True)
    request_date = fields.Datetime(string='Request Date',default=fields.Datetime.now,readonly=True)