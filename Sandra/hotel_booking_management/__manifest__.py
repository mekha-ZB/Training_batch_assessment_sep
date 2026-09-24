{
    'name': 'Hotel Booking Management',
    "summary": """training""",
    "description": """training""",
    "author": 'ZestyBeanz Technologies',
    "website": 'www.zbeanztech.com',

    'version': '1.0',
    'depends': ['base','mail'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'report/booking_report.xml',
        'report/booking_template.xml',
        'views/hotel_booking_views.xml',
        'views/hotel_customers_views.xml',
        'views/hotel_room_views.xml',
        'views/hotel_mail_template.xml',

    ],
    'installable': True,
    "auto_install": False,
    'application': True,
}