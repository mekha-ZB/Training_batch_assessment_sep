from odoo import models, fields
from odoo.exceptions import ValidationError


class CancellationWizard(models.TransientModel):
    _name = 'cancellation.history.wizard'
    _description = 'Cancellation history Wizard'

    reason = fields.Text(string="Reason for Cancellation")
    
    def reason_submit(self):
        pass