from odoo import models, fields, api
from odoo . exceptions import UserError
import base64


class SalonAppointment(models.Model):
    _name = 'salon.appointment'
    _description = 'Salon Appointment  '
    _rec_name = 'customer_id'


    _inherit = ['mail.thread', 'mail.activity.mixin']


    appointment_number = fields.Char(
        string='Appointment Number',
        copy=False,
        default='New',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        string='Customer Name',
        domain=[('user_role', '=', 'customer')],
        required=True
    )

    stylish_id = fields.Many2one(
        'res.partner',
        string='Stylish Name',
        required=True
    )
    stylish_list_ids = fields.Many2many(
        'res.partner',
        string='Stylish Names',
    )

    service_id = fields.Many2one(
        'salon.service',
        string='Selected Service',
        required=True
    )

    # is_receptionist = fields.Boolean(
    #     string='Is Receptionist',
    #     compute='_compute_is_receptionist',
    # )

    # is_supervisor = fields.Boolean(
    #     string='Is Receptionist',
    #     compute='_compute_is_receptionist',
    # )

    state = fields.Selection(
        selection=[
            ('booked', 'Booked'),
            ('cancelled', 'Cancelled'),
            ('cancellation requested', 'Cancellation Requested'),
        ],
        string='Status',
        default='booked',
        required=True,
    )
    appointment_date_time = fields.Datetime(
        string='Appointment Date',
    )

    notes = fields.Text(
        string='Notes',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('appointment_number', 'New') == 'New':
                val['appointment_number'] = self.env['ir.sequence'].next_by_code('appointment.id') or 'New'
            return super().create(vals_list)

    @api.onchange('service_id')
    def onchange_stylish_lists(self):
        for rec in self:
            if rec.service_id:
                rec.stylish_list_ids = rec.service_id.stylist_ids.ids

    def send_mail(self):
        self.ensure_one()

        # Email template
        template = self.env.ref(
            'salon_appointment_booking.mail_template_salon_details'
        )

        # PDF report
        report = self.env.ref(
            'salon_appointment_booking.action_salon_details_report'
        )

        # Generate PDF
        pdf_content, content_type = report._render_qweb_pdf(
            'salon_appointment_booking.action_salon_details_report',
            res_ids=self.ids
        )

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.customer_id.name} - Appointment Confirmation.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'salon.appointment',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        # Open email composer
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Email',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'salon.appointment',
                'default_res_ids': [self.id],
                'default_template_id': template.id,
                'default_attachment_ids': [
                    (6, 0, [attachment.id])
                ],
                # 'default_composition_mode': 'comment',
            },
        }


    # def send_mail(self):
    #     self.ensure_one()
    #     ctx = {
    #         'default_model': 'salon.appointment',
    #         'default_res_ids': self.ids,
    #         'default_composition_mode': 'comment',
    #         'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
    #         'email_notification_allow_footer': True,
    #         'hide_mail_template_management_options': True,
    #         'default_partner_ids': self.customer_id.ids,
    #         'default_reply_to': self.customer_id.email,
    #         'force_email': True,
    #     }
    #
    #     if not self.env.context.get('hide_default_template'):
    #         mail_template = self.env.ref(
    #             'salon_appointment_booking.mail_template_salon_details',
    #             raise_if_not_found=False,
    #         )
    #
    #         if mail_template:
    #             ctx.update({
    #                 'default_template_id': mail_template.id,
    #             })
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Compose Email',
    #         'res_model': 'mail.compose.message',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': ctx,
    #     }


    @api.onchange('stylish_id', 'appointment_date_time')
    def _onchange_check_stylish_appointment(self):
        if not self.stylish_id or not self.appointment_date_time:
            return

        existing = self.search([
            ('stylish_id', '=', self.stylish_id.id),
            ('appointment_date_time', '=', self.appointment_date_time),
            ('state', '!=', 'cancelled'),
        ], limit=1)

        if existing:
            return {
                'warning': {
                    'title': 'Stylist Already Booked',
                    'message': (
                        'This stylist already has another appointment '
                        'at the selected date and time.'
                    ),
                }
            }

    # @api.depends()
    # def _compute_is_receptionist(self):
    #     for salon in self:
    #         if self.env.user.has_group(
    #                 'salon_appointment_booking.group_receptionist'
    #         ):
    #             salon.is_receptionist = True
    #         else:
    #             salon.is_receptionist = False

    # @api.depends()
    # def _compute_is_supervisor(self):
    #     for salon in self:
    #         if self.env.user.has_group(
    #                 'salon_appointment_booking.group_supervisor'
    #         ):
    #             salon.is_supervisor = True
    #         else:
    #             salon.is_supervisor = False

    def action_request_cancellation(self):
        for appointment in self:
            if appointment.state != 'booked':
                raise UserError(
                    "Only booked appointments can request cancellation."
                )
            appointment.state = 'cancellation requested'

    def action_approved(self):
        for appointment in self:
            appointment.state = 'cancelled'

    def action_rejected(self):
        for appointment in self:
            appointment.state = 'booked'

    def unlink(self):
        for appointment in self:
            if (
                    appointment.state == 'booked'
                    and self.env.user.has_group(
                'salon_appointment_booking.group_supervisor'
            )
            ):
                raise UserError(
                    "A Floor Supervisor cannot Delete A booked appointment."
                )
        return super().unlink()
