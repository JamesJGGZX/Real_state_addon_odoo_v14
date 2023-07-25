from odoo import models, fields


#Creando un modelo (tabla de la base de datos) a partir de una clase
class Autor(models.Model):
    _name = 'autor' #nombre de la tabla que se va a generar
    _description = 'El objeto Autor'

    name = fields.Char(string="Nombre", required=True)