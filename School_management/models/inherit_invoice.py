from odoo import fields, models

class down(models.TransientModel):
    _inherit = "sale.advance.payment.inv"


    """this function is used to pass the Value from sale order to Downpayment Invoice """

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(down, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        invoice_vals["in_invoice_desc"] = order.invoice_desc
        return invoice_vals
        

class Inheritinvoice(models.Model):
    _inherit = "account.move"

    in_invoice_desc = fields.Char(string="Invoice Descirption")