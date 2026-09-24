from odoo import fields, models,api


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'


    _rec_name = 'room_type'
    room_number = fields.Char(string='Room Number', required=True, copy=False, readonly=True, default='New' )
    room_type = fields.Selection([('single', 'Single'),('double', 'Double'),('suite', 'Suite')], string='Room Type', required=True, default='single')
    rate_per_night = fields.Float(string='Rate Per Night', required=True)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('room_number', 'New') == 'New':
                vals['room_number'] = self.env['ir.sequence'].next_by_code('hotel.room') or 'New'
        return super().create(vals_list)