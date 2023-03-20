from odoo import api, fields, models


class stock(models.Model):
    _inherit = "stock.move"

    weight = fields.Integer(string="Weight")

    """create the _get_new_picking_values function to pass the value from sale_order to Delivery"""

    def _get_new_picking_values(self):
        vals = super(stock, self)._get_new_picking_values()
        in_delivery_desc = self.group_id.sale_id.delivery_desc
        vals["in_delivery_desc"] = (
            any(rule.propagate_carrier for rule in self.rule_id) and in_delivery_desc
        )
        return vals

    """create the _prepare_procurement_values function to pass the value from sale_order to Manufacturing"""

    def _prepare_procurement_values(self):
        res = super()._prepare_procurement_values()
        res["Manufacturing_desc"] = self.sale_line_id.order_id.Manufacturing_desc
        return res

    def _prepare_procurement_values(self):
        proc_values = super()._prepare_procurement_values()
        proc_values["purchase_desc"] = self.sale_line_id.order_id.purchase_desc
        return proc_values

    """create the get_data function to pass the value from sale_order_line to Delivery order"""

    def get_data(self):
        for move in self:
            picking = move.picking_id
            sale_order = self.env["sale.order"].search(
                [("procurement_group_id", "=", picking.group_id.id)], limit=1
            )
            for line in sale_order.order_line:
                if line.product_id.id != move.product_id.id:
                    continue
                move.update(
                    {
                        "weight": line.weight,
                    }
                )
