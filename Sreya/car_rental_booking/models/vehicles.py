from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CarDetails(models.Model):
    _name = 'vehicle.details'
    _description = 'Car Details'
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name = 'model'
    
    vehicle_type = fields.Char(string="Vehicle Type")
    model = fields.Char(string="Model")
    plate_number = fields.Char(string="Plate Number")
    daily_rate = fields.Float(string="Daily Rate")
    ref = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    
    @api.constrains('daily_rate')
    def _daily_rate(self):
        for record in self:
            if record.daily_rate < 0:
                raise ValidationError("Daily rate cannot be negative")
            
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('ref','New') == 'New':
                val['ref'] = self.env['ir.sequence'].next_by_code('vehicle.id') or 'New'
        return super(CarDetails, self).create(vals_list)