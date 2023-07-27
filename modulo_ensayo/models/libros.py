from odoo import models, fields, api
from odoo.exceptions import ValidationError


#Creando un modelo (tabla de la base de datos) a partir de una clase
class Libros(models.Model):
    _name = 'libros' #nombre de la tabla que se va a generar
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = '''Esta clase hace referencia al objeto Libros, 
                   lo que sigue después de esto es la definición de sus atributos en este caso los campos'''

    supervisor_id = fields.Many2one(comodel_name="hr.employee",string="Supervisor")
    name = fields.Char(string="Nombre del libro", required=True, tracking=True) #nombre del campo que es de tipo cadena
    editorial = fields.Char(string="Editorial", required=True)
    isbn = fields.Char(string="ISBN", required=True)
    autor_id = fields.Many2one(comodel_name="autor", string="Autor", required=True)
    autor_last_name = fields.Char(related="autor_id.last_name", string="Apellido del autor", required=True)
    image = fields.Binary(string="Imagen")
    categoria_id = fields.Many2one(comodel_name="categoria.libro")
    state = fields.Selection([("draft","Borrador"),("published","Publicado")], default="draft")
    description = fields.Char(string="Descripcion", compute="_compute_descripcion")
    
    @api.constrains('name')
    def _check_campo_unico(self):
        for record in self:
            # Verificar si ya existe un registro con el mismo valor
            if self.env['libros'].search([
                # Aqui se colocan los campos que se quieren evaluar para que estos no se repitan
                    ('name', '=', record.name)
                ]):
                raise ValidationError("El nombre del libro ya existe")

    #Con la palabra reservada api.depends se establecen dependencias en los campos, de modo que sin la necesidad de guardar el registro el dato del campo se guarda igualmente
    @api.depends('name','isbn')
    #Estos son datos computados donde se concatenan las variables que se encuentran definidas dentro de la funcion
    def _compute_descripcion(self):
        self.description = str(self.name) + ' | ' + str(self.isbn) + ' | ' + str(self.autor_id.name) + ' | ' + str(self.categoria_id.name)

    #En esta funcion se guarda el boton de publicacion
    def boton_publicar(self):
        self.state='published'

    #En esta funcion se guarda el boton de borrar
    def boton_borrar(self):
        self.state='draft'

class CategoriaLibro(models.Model):
    _name = 'categoria.libro'
    _description = '''Esta clase hace referencia al objeto CategoriaLibro, 
                       lo que sigue después de esto es la definición de sus atributos en este caso los campos'''

    name = fields.Char(string="Nombre de la categoria")