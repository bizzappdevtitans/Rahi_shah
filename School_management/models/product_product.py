from odoo import fields, models


class Product(models.Model):
    _inherit = "product.product"

    sale_order_ids = fields.One2many(
        "sale.order.line",
        "product_id",
        string="Sale",
        limit=5,
        domain=[("state", "=", "sale")],
    )
    purchase_order_ids = fields.One2many(
        "purchase.order.line",
        "product_id",
        string="Purchase",
        limit=5,
        domain=[("state", "=", "purchase")],
    )
