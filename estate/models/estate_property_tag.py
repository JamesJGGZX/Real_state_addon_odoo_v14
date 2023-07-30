from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "real.estate_tag"
    _description = "The Real Estate Module Tag Master"

    name = fields.Char(string="Name",required=True)