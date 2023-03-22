from odoo import fields, models


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

    """create the _get_new_picking_values function to pass the value from sale_order_line to Delivery"""

    def _get_new_picking_values(self):
        vals = super(stock, self)._get_new_picking_values()

        for move in self:
            if not move.sale_line_id or not move.sale_line_id.product_id.weight_done:
                continue
            move.weight = move.sale_line_id.weight
        return vals

        """create the _action_done function to pass the value from sale_order_line to Delivery order"""

    def _action_done(self, cancel_backorder=False):
        vals = super(stock, self)._action_done()
        for move in self:
            if not move.sale_line_id or not move.sale_line_id.product_id.weight_done:
                continue
            move.sale_line_id.weight = move.weight
        return vals