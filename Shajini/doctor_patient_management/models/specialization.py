from odoo import fields, models


class Specialization(models.Model):
    _name = 'specialization'
    _description = 'Specialization'
    _rec_name = 'specialization_name'

    specialization_name = fields.Char(string='Specialization')