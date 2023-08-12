from odoo import models, fields

class EstateProperty(models.Model):
    _inherit = "real.estate"

    def sold_property(self):
        """Override the sold_property method to add custom logic"""
    
        res = super(EstateProperty, self).sold_property()
    
        # Obtener el partner_id y el move_type
        partner_id = self.env.user.property_ids.buyer_id
        move_type = 'out_invoice'
    
        # Crear valores para la factura vacía
        move_values = {
            'partner_id': partner_id,
            'move_type': move_type,
        }
    
        # Crear el objeto account.move vacío
        new_move = self.env['account.move'].create(move_values)
    
        # Agregar líneas de factura
        # Aqui se calcula el 6% del precio de venta
        invoice_line_values = [
            {
                'name': 'Selling Price',
                'quantity': 1,
                'price_unit': self.selling_price * 0.06,
                'move_id': new_move.id,
            },
        # Aqui se calculan las 100 tasas administrativas
            {
                'name': 'Administrative Fees',
                'quantity': 1,
                'price_unit': 100.00,
                'move_id': new_move.id,
            },
        ]
        
        lines = [(0, 0, line_values) for line_values in invoice_line_values]
        
        new_move.write({
            'invoice_line_ids': lines,
        })
    
        # Aquí puedes agregar lógica personalizada de negocio
    
        return res
    