from odoo import api, fields, models


class HotelRoomType(models.Model):

    _name = "hotel.room.type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hotel Room Type"
    _rec_name="room_sequence"

    room_sequence = fields.Char(
        "Room Reference", required=True, index=True, copy=False, default="New"
    )
    floor_id = fields.Many2one(
        "room.floor",
        "Floor No",
    )
    room_type = fields.Selection(
        [
            ("single Room", "Single Room"),
            ("twin Room", "Twin Room"),
            ("king Room", "King Room"),
            ("queen Room", "Queen Room"),
            ("interconnecting Room", "Interconnecting Room"),
            ("adjoining Room", "Adjoining Room"),
        ]
    )
    room_price = fields.Integer(string="Room Price",tracking=True)
    room_status = fields.Selection(
        [("available", "Available"), ("booked", "Booked")],
        default="available",
    )
    room_photo = fields.Binary(string="Photo")
    description = fields.Text()
    room_capacity = fields.Integer(string="Capacity")

   

    @api.model
    def create(self, vals):
        """Generate the sequence """
        if vals.get("room_sequence", ("New")) == ("New"):
            vals["room_sequence"] = self.env["ir.sequence"].next_by_code(
                "hotel.room.type"
            )
            record = super(HotelRoomType, self).create(vals)
        return record