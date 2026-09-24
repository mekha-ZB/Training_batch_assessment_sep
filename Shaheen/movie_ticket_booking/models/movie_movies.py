from odoo import fields,api,models

class MoiveMovies(models.Model):
    _name = 'movie.movies'
    _description = 'Movies available'
    _rec_name = 'movie_name'
    
    movie_name = fields.Char(string='Movie Name')
    movie_runtime = fields.Float(string='Run Time')
    movie_halls = fields.Many2one('movie.halls',string='On Auditorium')
    
    