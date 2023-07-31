from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstatePropertyType(models.Model):
    _name = "real.estate_tag"
    _description = "The Real Estate Module Tag Master"

    name = fields.Char(string="Name",required=True)

    @api.constrains("name")
    def _check_unique_property_label(self):
        for record in self:
            existing_property = self.search([("name", "=", record.name)])
            if len(existing_property) > 1:
                raise ValidationError("The property label must be unique.")