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
    
    @api.onchange('movie_id')
    def fetch_runtime_hall_id(self):
        if not self.movie_id:
            self.run_time = False
            self.hall_id = False
            return
        self.run_time = self.movie_id.movie_runtime
        self.hall_id = self.movie_id.movie_halls

            
            
        