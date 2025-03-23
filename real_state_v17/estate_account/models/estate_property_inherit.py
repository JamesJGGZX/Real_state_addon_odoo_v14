# -*- coding: utf-8 -*-

from odoo import models, Command
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for property in self:
            if not property.buyer_id:
                raise UserError("Please set a buyer for the property before marking it as sold.")

            # Determinar el tipo de movimiento
            move_type = 'out_invoice'  # Factura de cliente

            # Buscar el diario correspondiente
            journal = self.env['account.journal'].search([
                ('type', '=', 'sale'),
                # ('company_id', '=', property.company_id.id),
            ], limit=1)

            if not journal:
                raise UserError("No sales journal found for the company's accounting configuration.")

            # Crear la factura
            invoice_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': move_type,
                'journal_id': journal.id,
                'invoice_line_ids': [
                    # Línea de comisión (6% del precio de venta)
                    Command.create({
                        'name': 'Commission (6%)',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    # Línea de tarifa administrativa fija de 100
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            }

            self.env['account.move'].create(invoice_vals)

        return super().action_sold()
