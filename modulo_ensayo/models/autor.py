from odoo import models, fields


#Creando un modelo (tabla de la base de datos) a partir de una clase
class Autor(models.Model):
    _name = 'autor' #nombre de la tabla que se va a generar
    _description = '''Esta clase hace referencia al objeto Autor, 
                   lo que sigue después de esto es la definición de sus atributos en este caso los campos'''
    _rec_name = 'last_name' #Retorna el apellido del autor que se encuentra guardado por default en la base de datos

    name = fields.Char(string="Nombre", required=True)
    last_name = fields.Char(string="Apellido", required=True)