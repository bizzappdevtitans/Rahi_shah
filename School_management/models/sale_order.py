from odoo import fields, models, api


class InheritDesc(models.Model):
    _inherit = "sale.order"

    description = fields.Char(string="Descirption")
    payment_mode = fields.Selection(
        [
            ("online", "Online"),
            ("cash", "Cash"),
        ]
    )

    delivery_desc = fields.Char(string="Delivery Descirption")

    invoice_desc = fields.Char(string="Invoice Descirption")

    project_desc = fields.Char(string="project Descirption")

    purchase_desc = fields.Char(string="Purchase Descirption")

    Manufacturing_desc = fields.Char(string="Manufacturing")

    display_delivery_address = fields.Boolean(
        "Display Address", related="partner_id.display_delivery_address", store=True
    )

    """create the _prepare_invoice function to pass the value from sale_order to Regular Invoivce"""

    def _prepare_invoice(self):
        rec = super(InheritDesc, self)._prepare_invoice()
        rec["in_invoice_desc"] = self.invoice_desc
        return rec

    """create the _prepare_analytic_account_data function to pass the value from sale_order to Project and Task model"""

    def _prepare_analytic_account_data(self, prefix=None):
        vals = super(InheritDesc, self)._prepare_analytic_account_data(prefix)
        vals["project_desc"] = self.project_desc
        return vals

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        val = super(InheritDesc, self).onchange_partner_id()
        delivery_type = self.partner_id.child_ids.filtered(
            lambda x: x.type == "delivery" and x.display_delivery_address
        )
        self.partner_shipping_id = delivery_type[:1]
        print("\n\n\n\n ----- delivery type ----", delivery_type)
        if not delivery_type:
            other_type = self.partner_id.child_ids.filtered(
                lambda x: x.type == "other" and x.display_delivery_address
            )
            self.partner_shipping_id = other_type[:1]
            print("\n\n\n\n ----- Other type ----", other_type)
            return val