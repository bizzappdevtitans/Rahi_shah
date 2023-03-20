from odoo import fields, models


class InheritPur(models.Model):
    _inherit = "product.template"

    weight_done = fields.Boolean(string="weight Done", store=True)
