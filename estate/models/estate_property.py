from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "real.estate"
    _description = "The Real Estate Module Master"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        string="Garden Orientation",
        required=True
    )

    @api.constrains('date_availability')
    def _check_duplicate_field(self):
        for record in self:
            if self.env['real.estate'].search_count([('date_availability', '=', record.date_availability)]) > 1:
                raise ValidationError("The available date field already exists.")
            
    @api.constrains('expected_price')
    def _check_duplicate_field(self):
        for record in self:
            if self.env['real.estate'].search_count([('expected_price', '=', record.expected_price)]) > 1:
                raise ValidationError("The value of the sale price already exists.")