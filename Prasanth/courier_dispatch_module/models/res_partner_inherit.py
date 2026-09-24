from odoo import models,fields,api

class Respartnerinherit(models.Model):
    _inherit='res.partner'

    is_courier_incharge=fields.Boolean(string='Is Courier Incharge',default=False)
    is_customer=fields.Boolean(string='Is Customer',default=False)
    customer_booking_count=fields.Integer(string='Customer Booking Count',compute='_compute_customer_booking_count')
    
    @api.depends()
    def _compute_customer_booking_count(self):
        for rec in self:
            rec.customer_booking_count=self.env['pickup.booking'].search_count([('customer_id', '=', rec.id)])

    def action_view_customer_bookings(self):
        self.ensure_one()
        
        return{
            'type':'ir.actions.act_window',
            'name':'Customer Bookings',
            'res_model':'pickup.booking',
            'view_mode':'list,form',
            'domain':[('customer_id', '=', self.id)],
        }

        