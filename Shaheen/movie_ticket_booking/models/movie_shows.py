from odoo import fields,models,api
from datetime import datetime

class MovieShows(models.Model):
    _name = 'movie.shows'
    _description = 'shows available'
    _rec_name = 'movie_id'
    
    movie_id = fields.Many2one('movie.movies',string='Movie')
    show_date = fields.Datetime(string='Date')
    run_time = fields.Float(string='Run Time')
    hall_id = fields.Many2one('movie.halls',string='Hall')
    
    
    
    