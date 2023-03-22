from odoo import api, fields, models


class Inheritorderline(models.Model):
    _inherit = "sale.order.line"

    order_lines = fields.Char(string="Header")
    weight_done = fields.Boolean(
        string="weight Done", related="product_template_id.weight_done", store=True
    )

    weight = fields.Integer(string="Weight")

    def _prepare_order_line_procurement(self, group_id=False):
        vals = super(Inheritorderline, self)._prepare_order_line_procurement(
            group_id=group_id
        )
        vals.update(
            {
                "weight": self.weight,
            }
        )
        return vals
