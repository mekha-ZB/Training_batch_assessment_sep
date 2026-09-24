{
    'name': 'Gym Membership Tracking',
    'version': '1.0',
    'summary': 'Track gym memberships',
    'description': 'This module is used to track gym memberships.',
    'author': 'Zesty Beans',
    'category': 'fitness',
    'license': 'LGPL-3',
    'sequence': '2',
    'depends': ['base', 'contacts', 'mail'],

    'data': ['security/security_group.xml',
             'security/record_rule.xml',
             'security/ir.model.access.csv',

             'views/membership_details_views.xml',
             'views/membership_plan_views.xml',
             'views/res_partner_inherit_views.xml',

             'report/membership_card_report_template.xml',
             'report/membership_card_report_action.xml',

             'data/email_template.xml',
             'data/ir_cron_data.xml',
             'data/ir.sequence.xml',

             'views/menu.xml'],

    'installable': True,
    'application': True,
    'auto_install': False,

}
