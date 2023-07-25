from odoo import models, fields


#Creando un modelo (tabla de la base de datos) a partir de una clase
class Libros(models.Model):
    _name = 'libros' #nombre de la tabla que se va a generar
    _description = 'Objeto libro'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Nombre del libro", required=True, tracking=True) #nombre del campo que es de tipo cadena
    editorial = fields.Char(string="Editorial", required=True)
    isbn = fields.Char(string="ISBN", required=True)
    autor_id = fields.Many2one(comodel_name="autor", string="Autor", required=True)
    image = fields.Binary(string="Imagen")
    categoria_id = fields.Many2one(comodel_name="categoria.libro")

    _sql_contraints = [("name_uniq", "unique(name)", "¡¡El nombre del libro ya existe!!")]
    #Nombre del sql constraints
    #unique () los valores que no queremos que se dupliquen
    #Mensaje de error

class CategoriaLibro(models.Model):
    _name = 'categoria.libro'
    _description = 'Objeto categoria'

    name = fields.Char(string="Nombre de la categoria")