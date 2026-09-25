from odoo import models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class HospitalXlsxReport(models.AbstractModel):
    _name = 'report.doctor_patient_management.clinic_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard):

        sheet = workbook.add_worksheet('Student Report')
        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 14,
        })

        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
        })

        center_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
        })

        date_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })


        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 18)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 25)


        sheet.merge_range(
            'A1:E1',
            'Hospital Report',
            title_format
        )



        sheet.write(
            'A2',
            'From Date',
            header_format
        )

        sheet.write(
            'B2',
            str(wizard.from_date),
            date_format
        )

        sheet.write(
            'C2',
            'To Date',
            header_format
        )

        sheet.write(
            'D2',
            str(wizard.to_date),
            date_format
        )
        headers = [
            'Sequence Number',
            'Date and Time',
            'Reason For Visit',
            'Doctor',
            'Patient',


        ]

        for col, header in enumerate(headers):
            sheet.write(
                3,
                col,
                header,
                header_format
            )



        appointments = self.env['appointment'].search([
            ('date_and_time', '>=', wizard.from_date),
            ('date_and_time', '<=', wizard.to_date),
        ])



        if not appointments:
            raise UserError(
                f"Records not found from "
                f"{wizard.from_date.strftime('%d/%m/%Y')} "
                f"to "
                f"{wizard.to_date.strftime('%d/%m/%Y')}"
            )



        row = 4

        for appointment in appointments:

            sheet.write(
                row,
                0,
                appointment.seq_number or '',
                center_format
            )

            sheet.write(
                row,
                1,
                str(appointment.date_and_time or ''),
                center_format
            )

            sheet.write(
                row,
                2,
                appointment.reason_for_visit or 0,
                center_format
            )

            sheet.write(
                row,
                3,
                appointment.doctor_id.name or '',
                center_format
            )

            sheet.write(
                row,
                4,
                appointment.patient_id.name or '',
                center_format
            )




            row += 1