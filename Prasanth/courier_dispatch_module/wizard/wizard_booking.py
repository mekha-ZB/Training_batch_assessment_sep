from odoo import models,fields,api

class WizardBooking(models.TransientModel):
    _name = 'wizard.booking'
    _description = 'Wizard Booking'
    
    courier_id=fields.Many2one('res.partner',string='Courier Incharge')
    wizard_booking_ids=fields.One2many('wizard.booking.line','line_id',string='Wizard Bookings')


    def action_view_all_bookings(self):
      
        for rec in self.wizard_booking_ids:
            rec.booking_id.write({'courier_id':self.courier_id.id})

    @api.model   
    def default_get(self,fieldlist):
        res=super().default_get(fieldlist)
        active_ids=self.env.context.get('active_ids')
        lines=[]
        for rec in active_ids:
            courier_incharge=self.env['pickup.booking'].browse(rec)
            lines.append((0,0,{'booking_id':courier_incharge.id}))
        res['wizard_booking_ids']=lines

        return res

class WizardBookingLine(models.TransientModel):
    _name = 'wizard.booking.line'
    _description = 'Wizard Booking Line'
    
    line_id=fields.Many2one('wizard.booking',string='Wizard Booking')
    booking_id=fields.Many2one('pickup.booking',string='Booking')

    