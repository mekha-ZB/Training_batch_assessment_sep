from odoo import models
class StudentPdfReport(models.AbstractModel):
    _name = 'report.doctor_patient_management.report_managements_template'
    _description = 'Appointment PDF Report'
    def _get_report_values(self, docids, data=None):
        wizard = self.env['hospital.report.wizard'].browse(docids)
        appointments = self.env['appointment'].search([
            ('date_and_time', '>=', wizard.from_date),
            ('date_and_time', '<=', wizard.to_date),
        ])
        return {
            'doc_ids': wizard.ids,
            'doc_model': 'hospital.report.wizard',
            'docs': wizard,
            'appointments': appointments,
            'from_date': wizard.from_date,
            'to_date': wizard.to_date,
        }

