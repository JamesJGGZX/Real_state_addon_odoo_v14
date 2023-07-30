from odoo import models,fields

class HrEmploye(models.Model):
    _inherit = "hr.employee"

    is_supervisor = fields.Boolean(string="Es supervisor")