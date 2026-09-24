from odoo import models, fields


class SurveySurvey(models.Model):
    _inherit = "res.partner"

    user_role = fields.Selection([
        ('stylist', 'Stylist'),
        ('customer', 'Customer'),
        ('receptionist', 'Receptionist')
    ], string='User Role', default='stylist')