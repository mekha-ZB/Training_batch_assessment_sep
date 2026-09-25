from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    total_rentals = fields.Integer(string='Total No. of reantals',compute='compute_total_rentals')
    
    def compute_total_rentals(self):
        for partner in self:
            total = self.env['booking.details'].search_count([('customer_id', '=', partner.id)])
            partner.total_rentals = total
            return {
                'name': 'total rentals',
                'type': 'ir.actions.act_window',
                'view_mode': 'list',
                'res_model': 'booking.details',
                'domain': [('customer_id', '=', self.id)]

            }