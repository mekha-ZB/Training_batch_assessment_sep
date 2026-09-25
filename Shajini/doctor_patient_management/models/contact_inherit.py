from odoo import models, fields,api

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_doctor = fields.Boolean(string="Is Doctor")
    is_patient = fields.Boolean(string="Is Patient")
    total_visits = fields.Integer(string="Total Visits",compute="_compute_total_visits")

    @api.depends()
    def _compute_total_visits(self):
        appointment = self.env["appointment"]
        for partner in self:
            partner.total_visits = appointment.search_count([("patient_id", "=", partner.id),("state", "=", "completed")])


    def action_view_patient_appointments(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Appointments",
            "res_model": "appointment",
            "view_mode": "list,form",
            "domain": [("patient_id", "=", self.id),("state", "=", "completed")],
            "context": {"default_patient_id": self.id,},}