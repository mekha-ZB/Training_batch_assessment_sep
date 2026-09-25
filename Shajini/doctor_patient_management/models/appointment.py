from odoo import fields, models,api
from odoo.exceptions import UserError
from datetime import time
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'appointment'
    _description = 'Appointment'
    _rec_name = 'seq_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    patient_id = fields.Many2one('res.partner',string='Patient',required=True,domain=[("is_patient", "=", True),("is_company", "=", False)])
    doctor_id = fields.Many2one('res.partner',string='Doctor',required=True,domain=[("is_doctor", "=", True),("is_company", "=", False)])
    date_and_time = fields.Datetime(string='Date and Time',required=True)
    reason_for_visit = fields.Char(string='Reason For Visit')
    seq_number = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                             default=lambda self: 'New')
    booked_by = fields.Many2one("res.users",string="Booked By",default=lambda self: self.env.user,readonly=True,)
    specialization_id = fields.Many2one('specialization',string="Specialization")

    state = fields.Selection([
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('requested', 'Cancellation Requested'),
        ('cancelled', 'Cancelled'),], default='booked')

    cancellation_request_ids = fields.One2many('appointment.cancellation.request','appointment_id',string='Cancellation Requests')


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["seq_number"] = self.env["ir.sequence"].next_by_code("appointment")
        return super().create(vals_list)


    def send_mail(self):
        template = self.env.ref('doctor_patient_management.mail_template_appointment_detail')
        for record in self:
            if not record.patient_id.email:
                raise UserError("Patient email address is missing. ""Please add an email address to the patient.")

            template.send_mail(record.id,force_send=True,email_values={'email_to': record.patient_id.email,})

    @api.constrains("date_and_time")
    def _check_working_hours(self):
        for record in self:
            if not record.date_and_time:
                continue
            local_datetime = fields.Datetime.context_timestamp(record,record.date_and_time)
            appointment_time = local_datetime.time()
            start_time = time(9, 0)
            end_time = time(18, 0)
            if not start_time <= appointment_time <= end_time:
                raise ValidationError("Appointment time must be between 9:00 AM and 6:00 PM.")

    def action_open_reminder_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Send Appointment Reminders",
            "res_model": "appointment.reminder.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_appointment_ids": [(6, 0, self.ids)],
            },
        }



    def action_completed(self):
        for record in self:
            if self.state=='booked':
                record.state = 'completed'


    def action_requested(self):
        self.ensure_one()
        if self.state != 'booked':
            raise UserError("Cancellation request can only be made for booked appointments.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancellation Request',
            'res_model': 'appointment.cancellation.request.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref(
            'doctor_patient_management.view_cancellation_request_wizard_form').id,
            'target': 'new',
            'context': {'active_id': self.id,'active_model': 'appointment',}}

    def action_approved(self):
        for record in self:
            if self.state=='requested':
                record.state = 'cancelled'


    def action_cancelled(self):
        for record in self:
            if self.state=='requested':
                record.state = 'booked'


    def unlink(self):
        for record in self:
            if record.state == 'completed':
                if not self.env.user.has_group('doctor_patient_management.group_clinic_manager'):
                    raise ValidationError("Completed appointments can only be deleted by Clinic Manager.")
        return super().unlink()