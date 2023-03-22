from odoo import fields, models


class StockImmediate(models.TransientModel):
    _inherit = "stock.immediate.transfer"

    """create the process function to pass the value from Delivery to sale_order_line"""

    # def process(self):
    #     value = super(StockImmediate, self).process()
    #     data = self.env["stock.picking"].search([])
    #     for move in data.move_lines:
    #         sale = move.sale_line_id
    #         if sale:
    #             sale["weight"] = move.weight
        # record = self.env["sale.advance.payment.inv"].search([])
        # for rec in record:
        #     rec.create_invoices()
        #     return 
        # return value
 