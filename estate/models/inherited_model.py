from odoo import models, fields


class InheritedModel(models.Model):
    _name = "real.estate_inherited_model"
    _description = "The Real Estate Module inherited Master"

    property_ids = fields.One2many("real.estate", "seller_id", string="Users")
    