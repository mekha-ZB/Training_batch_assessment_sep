from odoo import models, fields,api



class SalonService(models.Model):
    _name = 'salon.service'
    _description = 'Salon Service  '
    _rec_name = 'service_name'



    service_name = fields.Char(
        string='Service Name',
       required=True
    )


    service_duration = fields.Float(
        string='duration',
        required=True
    )

    price=fields.Monetary(
        string='Price',
        required=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True
    )

    service_active=fields.Boolean(
        string='Active',
    )


    description=fields.Text(
        string='Description',
    )

    stylist_ids=fields.Many2many(
        'res.partner',
        string='Stylist',
        domain=[('user_role', '=', 'stylist')],
    )



