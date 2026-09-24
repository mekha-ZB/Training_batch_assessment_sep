from odoo import fields,models

class MovieSeats(models.Model):
    _name = 'movie.seats'
    _description = 'Manage seats available'
    _rec_name = 'seats_id'
    
    seats_id = fields.Char(string='Seat Number')
    seat_hall = fields.Many2one('movie.halls',string='Hall Name')
    # active = fields.Boolean(string='active')
    