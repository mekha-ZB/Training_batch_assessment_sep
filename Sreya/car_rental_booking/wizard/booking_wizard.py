from odoo import models, fields, api


class PropertyWizard(models.TransientModel):
    _name = 'booking.wizard'
    _description = 'Booking Wizard'

    reason = fields.Text(string="Reason For Cancellation")
  
    def action_confirm(self):
        pass