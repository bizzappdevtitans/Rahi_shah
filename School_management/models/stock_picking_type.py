from odoo import fields, models


class Inheritstockpicking(models.Model):
    _inherit = "stock.picking.type"

    invoice = fields.Boolean(string="Invoice")
