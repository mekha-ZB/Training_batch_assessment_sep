{
    "name": "Salon appointment Booking",
    "summary": """Salon appointment Booking""",
    "description": """
    Salon appointment Booking
    This module manages:
    -Stylist
    -Service
    -Appointment
    """,
    "author": 'Fathima Beevi S',
    "website": '',
    "category": "Service",
    "version": "19.0.0.1",
    "license": "LGPL-3",
    "depends": ["base",
                "mail",
                ],
    "data": [
        'security/ir.model.access.csv',
        'security/security_group.xml',
        'security/security_rules.xml',
        'Data/ir.sequence.xml',
        'reports/salon_report.xml',
        'reports/salon_report_templates.xml',
        'views/email_template_views.xml',
        'views/contact_inherit_views.xml',
        'views/salon_service_views.xml',
        'views/salon_appointment_views.xml',

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}