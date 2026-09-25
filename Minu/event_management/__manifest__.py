{
    'name':'Event Management',
    'version':'1.0',
    'author':'Minu',
    'description':'''Event Management''',
    'category':'Tools',
    'depends':['base','mail'],

    'data':[
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/security_rule.xml',
        'wizard/cancellation_history.xml',
        'data/ir.sequence.xml',
        'views/events.xml',
        'views/registrations.xml',
        'views/res_partner.xml',
        'reports/reports.xml',
        'reports/report_template.xml',
        'data/email_template.xml',
        
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False, 
    'license': 'LGPL-3',


}