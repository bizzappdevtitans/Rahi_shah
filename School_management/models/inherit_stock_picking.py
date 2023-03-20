from odoo import fields, models


class Inheritstock(models.Model):
    _inherit = "stock.picking"

    in_delivery_desc = fields.Char(string="Delivery Descirption")
