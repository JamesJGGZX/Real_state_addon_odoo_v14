from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "real.estate_type"
    _description = "The Real Estate Module Type Master"

    name = fields.Char(string="Title",required=True)