from odoo import api, fields, models


class TableBooking(models.Model):

    _name = "table.booking"
    _description = "Table Booking"
    _rec_name = "table_no"

    table_no = fields.Char(
        "Table No", required=True, index=True, copy=False, default="New"
    )
    capacity = fields.Integer(string="Capacity")

    availability = fields.Selection(
        [("available", "Available"), ("booked", "Booked")],
    )

    # Generate Sequence

    @api.model
    def create(self, vals):
        if vals.get("table_no", ("New")) == ("New"):
            vals["table_no"] = self.env["ir.sequence"].next_by_code("table.booking")
            record = super(TableBooking, self).create(vals)
        return record
