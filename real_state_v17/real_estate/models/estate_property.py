# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=lambda self: date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True, copy=False)
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area", store=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        """ Si el usuario marca el jardín, asignar valores por defecto.
            Si lo desmarca, limpiar los valores. """
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("¡No puedes cancelar una propiedad que ya ha sido vendida!")
            record.state = 'canceled'

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("¡No puedes vender una propiedad que ha sido cancelada!")
            if not record.offer_ids:
                raise UserError("¡No puedes vender una propiedad sin ofertas!")
            best_offer = max(record.offer_ids.mapped('price'), default=0)
            best_offer_obj = record.offer_ids.filtered(lambda o: o.price == best_offer)
            if best_offer_obj:
                record.selling_price = best_offer
                record.buyer_id = best_offer_obj.partner_id
            record.state = 'sold'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        """ Asegura que el selling_price no sea menor al 90% del expected_price. """
        for record in self:
            # Ignorar si el selling_price es 0 (propiedad aún no vendida)
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            # Calcular el 90% del precio esperado
            min_acceptable_price = record.expected_price * 0.9

            # Comparar con float_compare para evitar problemas de precisión
            if float_compare(record.selling_price, min_acceptable_price, precision_rounding=0.01) == -1:
                raise ValidationError(
                    "The selling price ({}) cannot be less than 90% of the expected price ({}).".format(
                        record.selling_price, min_acceptable_price
                    )
                )

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for property in self:
            if property.state not in ['new', 'canceled']:
                raise UserError("You can only delete properties that are New or Canceled.")
    