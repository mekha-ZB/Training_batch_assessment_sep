from odoo import fields,api,models

class MovieHalls(models.Model):
    _name = 'movie.halls'
    _description = 'Halls available'
    _rec_name = 'hall_name'
    
    hall_name = fields.Char(string='Halls')
    hall_seats_ids = fields.Many2many('movie.seats', string='Seats',compute="_total_seats_in_Audi")
    hall_seat_count = fields.Char(string='Seat Count',compute="_total_seats_in_Audi")
    
    
    @api.depends('hall_name')
    def _total_seats_in_Audi(self):
        for rec in self:
            if rec.hall_name:
                print('yes===============>',rec.id)
                # print(rec.hall_id.hall_seats_ids)
                total_seats = self.env['movie.seats'].search([('seat_hall','=',rec.id)])
                print('total_seats ---',total_seats)
                rec.hall_seats_ids = total_seats.ids
                rec.hall_seat_count = len(total_seats.ids)
            else:
                 rec.hall_seats_ids = False
                 rec.hall_seat_count = False
            