from odoo import fields, models


class Inheritstock(models.Model):
    _inherit = "stock.picking"

    in_delivery_desc = fields.Char(string="Delivery Descirption")
    invoice_create_id = fields.Many2one("stock.picking.type")
    invoice = fields.Boolean(string="Invoice", related="invoice_create_id.invoice")


    def button_validate(self):
        vals = super(Inheritstock, self).button_validate()
        record = self.env["sale.advance.payment.inv"].search([])
        for rec in record:
            rec.create_invoices()
        return vals

 
 

