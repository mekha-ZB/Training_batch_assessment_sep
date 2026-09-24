from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class ProductLineId(models.Model):
    _name = "product.line.id"
    _description = "Product Line Id"
    _rec_name="product_line_id"


    product_line_id=fields.Many2one('product.template',string="Product Name")
    pickup_id=fields.Many2one('pickup.booking',string="Pickup Booking")
    currency_id = fields.Many2one('res.currency', string='Currency')
    product_price=fields.Monetary(string="Price")
    product_quantity=fields.Integer(string="Quantity")
    product_weight=fields.Float(string="Weight(Kg)")
    total_price=fields.Monetary(string="Total Price",compute='_compute_product_total_price')

    @api.onchange('product_line_id')
    def _onchange_product_name(self):
        for rec in self:
            if rec.product_line_id:
                rec.product_price = rec.product_line_id.standard_price
    
    @api.depends('product_price','product_quantity')
    def _compute_product_total_price(self):
        for rec in self:
            rec.total_price = rec.product_price * rec.product_quantity

    @api.constrains('product_weight','product_price','product_quantity')
    def _constrains_product_weight_price_quantity(self):
        for rec in self:
            if rec.product_weight <= 0 or rec.product_price <= 0 or rec.product_quantity <= 0 :
                raise ValidationError(_("Product Weight, Price and Quantity Must Be Greater Than 0"))
         
    
        
        