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
    offer_ids = fields.One2many("real.estate_offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
    
    @api.constrains("name")
    def _check_unique_property_label(self):
        for record in self:
            existing_property = self.search([("name", "=", record.name)])
            if len(existing_property) > 1:
                raise ValidationError("The property type must be unique.")