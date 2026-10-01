from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        result = super().action_send_mail()

        registration_id = self.env.context.get('registration_id')

        if registration_id:
            registration = self.env['registration.details'].browse(registration_id)
            if registration.exists():
                registration.registration_status = 'completed'

        return result