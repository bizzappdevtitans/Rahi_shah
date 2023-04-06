from odoo import fields, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    advance_payment_method = fields.Selection(
        [
            ("delivered", "Regular invoice"),
            ("percentage", "Down payment (percentage)"),
            ("fixed", "Down payment (fixed amount)"),
        ],
        string="Create Invoice",
        required=True,
        help="""A standard invoice is issued with all the order lines ready for
        invoicing, according to their invoicing policy
        (based on ordered or delivered quantity).""",
    )

    def create_invoices(self):
        ctx = self.env.context.copy()
        if self._context.get("active_model") == "room.reservation":
            HotelFolio = self.env["room.reservation"]
            reservation = self.env["room.reservation"].browse(self._context.get("active_ids", []))
            ctx.update(
                {
                    'reservation_id': reservation.id,
                    'active_ids': reservation.sale_order_id.ids,
                    'active_id': reservation.sale_order_id.id,
                }
            )
        res = super(SaleAdvancePaymentInv, self.with_context(**ctx)).create_invoices()
        return res