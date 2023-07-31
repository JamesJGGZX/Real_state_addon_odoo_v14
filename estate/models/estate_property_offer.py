from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "real.estate_offer"
    _description = "The Real Estate Module offer Master"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="real.estate", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline")
    create_date = fields.Datetime(string="Create Date", default=fields.Datetime.now())
    backup_create_date = fields.Datetime(string='Backup Create Date')

    @api.constrains("price")
    def _check_positive_offer_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("The offer price must be strictly positive.")
    
    @api.onchange("create_date")
    def _onchange_create_date(self):
        self.backup_create_date = self.create_date

    @api.depends("backup_create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.backup_create_date or datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.backup_create_date = record.date_deadline - timedelta(days=record.validity)