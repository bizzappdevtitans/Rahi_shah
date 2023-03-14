from odoo import fields, models

class InheritPur(models.Model):
    _inherit = "purchase.order"

    purchase_desc = fields.Char(string="Purchase Descirption")