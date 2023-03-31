from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    # This method used for create invoice
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if self._context.get("room_booking"):
            folio = self.env["room.reservation"].browse(self._context["room_booking"])
            folio.write({"hotel_invoice_id": res.id, "invoice_status": "invoiced"})
        return res