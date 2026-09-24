{
    'name': 'Courier Dispatch Module',
    "summary": "Courier Dispatch Module",
    "version": "19.0.0.0",
    "author": "Zesty Beanz Technology (P) Ltd.",
    "license": "LGPL-3",
    "website": "http://www.zbeanztech.com",
    "description": "Welcome to our Courier Dispatch Module",
    'depends': ['base','contacts','product','sale','mail'],
    'data': [
        'security/courier_groups.xml',
        'security/ir.model.access.csv',
        'views/pickup_booking_views.xml',
        'views/res_partner_inherit_views.xml',
        'wizard/wizard_booking_views.xml',
        'data/ir.sequence.xml',
        'report/courier_report_action.xml',
        'report/courier_report_template.xml',
        'data/email_template.xml',
        'views/menus_views.xml',

    ],
    'test': [],
    'demo': [],
    'installation': True,
    'auto_install': False,
    'application': True,
}




