from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBookIssue(models.Model):
    _name = 'library.book.issue'
    _description = 'Library Book Issue'

    name = fields.Char(string='Issue Number',copy=False,default='New')
    book_id = fields.Many2one('library.book', string='Book')
    member_id = fields.Many2one('res.partner', string='Member')
    user_id = fields.Many2one('res.users', string='Librarian')
    issue_date = fields.Date(string='Issue Date')
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('cancel_requested', 'Cancellation Requested'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='issued', required=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('library.book.issue') or 'New'
        return super(LibraryBookIssue, self).create(vals_list)

    def action_send_email(self):
        self.ensure_one()
        lib = self.env.ref('library_management1.email_template_book_issue_slip', raise_if_not_found=False)
        if lib:
            lib.send_mail(self.id, force_send=True)
        return True

    def action_mark_returned(self):
        for rec in self:
            rec.state = 'returned'

    def action_request_cancel(self):
        for rec in self:
            rec.state = 'cancel_requested'

    def action_approve_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_reject_cancel(self):
        for rec in self:
            rec.state = 'issued'

    @api.constrains('book_id')
    def _check_book_availability(self):
        for record in self:
            if record.book_id and record.book_id.available_copies <= 0:
                raise ValidationError('No available copies left')



