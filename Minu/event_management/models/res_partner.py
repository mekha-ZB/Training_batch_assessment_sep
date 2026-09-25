from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit='res.partner'

    seat_capacity = fields.Integer(string='Capacity',copy = False)

    