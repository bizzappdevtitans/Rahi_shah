from odoo import fields, models


class Inheritorderline(models.Model):
    _inherit = "sale.order.line"

    order_lines = fields.Char(string="Header")
