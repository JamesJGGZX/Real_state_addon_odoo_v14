from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstatePropertyType(models.Model):
    _name = "real.estate_type"
    _description = "The Real Estate Module Type Master"
    _rec_name = 'name'
    _order = "name_asc"

    name = fields.Char(string="Title",required=True)
    property_ids = fields.One2many("real.estate","property_type_id")
    name_asc = fields.Integer("Sequence", default=1, help="Used to order stages. Lower is better.")

    @api.constrains("name")
    def _check_unique_property_label(self):
        for record in self:
            existing_property = self.search([("name", "=", record.name)])
            if len(existing_property) > 1:
                raise ValidationError("The property type must be unique.")