{
    'name': 'Doctor And Patient Management',
    "summary": "Summery",
    "version": "19.0.0.0",
    "author": "Zesty Beanz Technology (P) Ltd.",
    "license": "LGPL-3",
    "website": "http://www.zbeanztech.com",
    "description": """Description""",
    'depends': ['base','contacts','mail','report_xlsx'],
     'data': [
        'security/groups.xml',
        'security/rule.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',


        'report/action.xml',
        'report/template.xml',
        'report/appointment_pdf_action.xml',
        'report/appointment_pdf_template.xml',
        'data/template.xml',
        'views/appointment_views.xml',
        'views/contact_inherit.xml',
        'views/reporting_views.xml',
        'views/specialization_views.xml',
        'wizard/reminder_wizard_views.xml',
        'wizard/xlsx_action.xml',
        'wizard/report_wizard_views.xml',
        'wizard/cancellation_wizard_views.xml',

        ],
    'test': [],
    'demo': [],
    'installation': True,
    'auto_install': False,
    'application': True,
}




