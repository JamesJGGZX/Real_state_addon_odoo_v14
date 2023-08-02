from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError
from datetime import date, timedelta
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "real.estate"
    _description = "The Real Estate Module Master"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability From",
        default=lambda self: date.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
        required=True,
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="new",
        required=True,
    )
    property_type_id = fields.Many2one(
        comodel_name="real.estate_type", string="Property Type"
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users", string="Salesman", index=True, default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(comodel_name="real.estate_tag", string="Tags")
    offer_ids = fields.One2many("real.estate_offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total Area(sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price')

    @api.constrains("selling_price")
    def _check_minimum_sale_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                expected_price = self.env["real.estate"].search([("id", "=", record.id)]).expected_price
                minimum_price = expected_price * 0.9
                if float_compare(record.selling_price, minimum_price, precision_digits=2) == -1:
                    raise ValidationError("The sale price cannot be less than 90% of the expected price.")
    
    @api.constrains("expected_price")
    def _check_positive_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("The expected price must be strictly positive.")
    
    def cancel_property(self):
        if self.state == "sold":
            raise exceptions.UserError("You cannot cancel a sold property.")
        else:
            self.state = "canceled"

    def sold_property(self):
        if self.state == "canceled":
            raise exceptions.UserError("You cannot sell a canceled property.")
        else:
            self.state = "sold"


    @api.onchange("garden")
    def _onchange_jardin(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.constrains("date_availability")
    def _check_duplicate_field(self):
        for record in self:
            if (
                self.env["real.estate"].search_count(
                    [("date_availability", "=", record.date_availability)]
                )
                > 1
            ):
                raise ValidationError("The available date field already exists.")

    @api.constrains("expected_price")
    def _check_duplicate_field(self):
        for record in self:
            if (
                self.env["real.estate"].search_count(
                    [("expected_price", "=", record.expected_price)]
                )
                > 1
            ):
                raise ValidationError("The value of the sale price already exists.")
