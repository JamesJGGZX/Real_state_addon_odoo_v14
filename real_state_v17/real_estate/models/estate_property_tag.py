# -*- coding: utf-8 -*-

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.')
    ]
    