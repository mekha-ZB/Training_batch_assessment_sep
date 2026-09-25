from odoo import fields, models
from odoo.exceptions import UserError


class CancellationRequestWizard(models.TransientModel):
    _name = 'appointment.cancellation.request.wizard'
    _description = 'Cancellation Request Wizard'

    reason = fields.Text(string='Cancellation Reason',required=True)
    def action_confirm(self):
        self.ensure_one()
        appointment_id = self.env.context.get('active_id')
        if not appointment_id:
            raise UserError("Appointment not found.")
        appointment = self.env['appointment'].browse(appointment_id)
        if appointment.state != 'booked':
            raise UserError("Cancellation request can be created only for Booked appointments.")
        self.env['appointment.cancellation.request'].create({'appointment_id': appointment.id,'requested_by': self.env.user.id,'reason': self.reason,})
        appointment.state = 'requested'
        return {'type': 'ir.actions.act_window_close'}
