from odoo import fields, models


class HotelRoom(models.Model):

    _name = "hotel.room"
    _description = "Hotel Room"
    _rec_name="floor_id"

    floor_id = fields.Many2one(
        "room.floor",
        "Floor No",
        # help="At which floor the room is located.",
        # ondelete="restrict",
    )
    adult = fields.Integer(string="Max Adult")
    child = fields.Integer(string="Max Chid")
    room_status = fields.Selection(
        [("available", "Available"), ("booked", "Booked")],
        default="available",
    )
    room_capacity = fields.Integer(string="Capacity")
