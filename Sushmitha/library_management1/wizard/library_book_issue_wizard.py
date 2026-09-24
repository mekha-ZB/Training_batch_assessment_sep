from odoo import models, fields, api

class LibraryBookIssueWizard(models.TransientModel):
    _name = 'library.book.issue.wizard'
    _description = 'Multiple Books Returned Wizard'

    issue_ids = fields.Many2many('library.book.issue', string='Selected Issues')

    @api.model
    def default_get(self, fields_list):
        res = super(LibraryBookIssueWizard, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            res['issue_ids'] = [(6, 0, active_ids)]
        return res

    def action_multiple_book_return(self):
        for rec in self.issue_ids:
            if rec.state == 'issued':
                rec.state = 'returned'
        return {'type': 'ir.actions.act_window_close'}