from odoo import models, fields


class StudentReportWizard(models.TransientModel):
    _name = 'hospital.report.wizard'
    _description = 'Hospital Report Wizard'


    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    check = fields.Boolean(string='Xlsx Report')

    def action_print_xlsx(self):
        if self.check==True:
            return self.env.ref('doctor_patient_management.hospital_xlsx_report').report_action(self)
        else:
            return self.env.ref('doctor_patient_management.report_managements_service').report_action(self)