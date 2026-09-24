{
    'name': 'Movie Ticket Booking',
    'version': '1.1',
    'category': 'Movie Booking',
    'summary': 'This module helps to manage and book movie tickets',
    'description': '''
        Movie Tickets Booking and Management System
    ''',
    'depends': ['base','contacts','account','mail'],

    'data': [
    
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        
        'data/booking_sequence.xml',
        'data/movie_mail_template.xml',
        
        'views/movie_menu.xml',
        'views/movie_booking_views.xml',
        'views/movie_hall_views.xml',
        'views/movie_movies_views.xml',
        'views/movie_seats_views.xml',
        'views/movie_shows_views.xml',
        
        'report/booked_ticket_template.xml',
    ],

    'installable': True,
    'application': True,
}
