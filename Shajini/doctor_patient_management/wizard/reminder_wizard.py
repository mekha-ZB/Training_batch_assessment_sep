from odoo import fields, models


class AppointmentReminderWizard(models.TransientModel):
    _name = "appointment.reminder.wizard"
    _description = "Appointment Reminder Wizard"

    appointment_ids = fields.Many2many("appointment",string="Appointments",required=True,)

    def action_send_reminders(self):
        template = self.env.ref("doctor_patient_management.mail_template_appointment_detail")

        for appointment in self.appointment_ids:
            template.send_mail(appointment.id,force_send=True,email_values={'email_to': appointment.patient_id.email,})

        return {
            "type": "ir.actions.act_window_close"
        }