from odoo import models, fields,api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Books'

    name = fields.Char(string='Book Title')
    author = fields.Char(string='Author Name')
    total_copies = fields.Integer(string='Total Copies')
    available_copies = fields.Integer(string='Available Copies',compute='_compute_available_copies')
    issue_ids = fields.One2many('library.book.issue', 'book_id', string='Book Issues')

    @api.depends('total_copies', 'issue_ids.state')
    def _compute_available_copies(self):
        for rec in self:
            issued_cnt = len(rec.issue_ids.filtered(lambda x: x.state == 'issued'))
            rec.available_copies = max(0, rec.total_copies - issued_cnt)
