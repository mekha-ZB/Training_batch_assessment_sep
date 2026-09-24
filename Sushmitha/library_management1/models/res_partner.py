from odoo import models, fields
class ResPartner(models.Model):
    _inherit = 'res.partner'

    issued_books_count = fields.Integer(string='Issued Books Count', compute='_compute_issued_books_count')
    def _compute_issued_books_count(self):
        issue_obj = self.env['library.book.issue']
        for rec in self:
            if isinstance(rec.id, int) and rec.id:
                rec.issued_books_count = issue_obj.search_count([
                    ('member_id', '=', rec.id),
                    ('state', '=', 'issued')
                ])
            else:
                rec.issued_books_count = 0

    def action_view_issued_books(self):
        self.ensure_one()
        return {
            'name': 'Issued Books',
            'type': 'ir.actions.act_window',
            'res_model': 'library.book.issue',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id), ('state', '=', 'issued')],
            'context': {'default_member_id': self.id},
        }

