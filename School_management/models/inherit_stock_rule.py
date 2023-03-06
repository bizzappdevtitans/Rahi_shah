from odoo import fields, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    """This function is used to pass the value from sale_order to Manufacturing"""

    def _prepare_mo_vals(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
        bom,
    ):
        res = super()._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        res["Manufacturing_desc"] = values.get("Manufacturing_desc")
        return res
