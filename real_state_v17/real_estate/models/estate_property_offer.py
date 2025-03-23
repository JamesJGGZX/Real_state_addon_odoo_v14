# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True,
        string="Property Type"
    )

    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """ Calcula la fecha límite sumando la fecha de creación + validez """
        for record in self:
            create_date = record.create_date or fields.Date.today()  # Fallback en caso de que create_date sea None
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """ Permite modificar la validez (`validity`) si el usuario cambia la fecha límite (`date_deadline`) """
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7  # Si no hay fecha de creación, se usa el valor por defecto

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['sold', 'canceled']:
                raise UserError("¡No puedes aceptar una oferta en una propiedad vendida o cancelada!")
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("¡Ya hay una oferta aceptada para esta propiedad!")

            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

            # Si la oferta rechazada era la que estaba en selling_price, buscar otra oferta aceptada
            accepted_offer = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                record.property_id.selling_price = accepted_offer.price
            else:
                record.property_id.selling_price = 0  # Si no hay oferta aceptada, se pone en 0
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_price = vals.get('price')

            if property_id and offer_price:
                property_rec = self.env['estate.property'].browse(property_id)

                # Verificar si hay ofertas existentes con precio mayor o igual
                existing_offer = self.search([
                    ('property_id', '=', property_id),
                    ('price', '>=', offer_price)
                ], limit=1)

                if existing_offer:
                    raise ValidationError("The offer price must be higher than all existing offers.")

                # Cambiar el estado de la propiedad
                property_rec.state = 'offer_received'

        # Crear todos los registros al final, en un solo llamado
        return super().create(vals_list)
    