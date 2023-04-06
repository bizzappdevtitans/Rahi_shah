from odoo import api, models, fields
from odoo.exceptions import ValidationError


class Roomcapacity(models.TransientModel):
    _name = "room.capacity.wizard"

    def _get_default_room(self):
        return self.env["hotel.room.type"].browse(self.env.context.get("active_ids"))

    room_ids = fields.Many2many(
        "hotel.room.type", string="Room", default=_get_default_room
    )
    adult = fields.Integer(string="Max Adult")
    child = fields.Integer(string="Max Chid")
    room_capacity = fields.Integer(string="Capacity", compute="_cal_total_capacity")

    """create the set_room_capacity function to set the value for capacity field 
    when Add the Capacity and click on button after that capacity field value is filled out"""

    def set_room_capacity(self):
        for record in self:
            if record.room_ids:
                for room in record.room_ids:
                    room.room_capacity = self.room_capacity

    """create the update_room_capacity function to Update the Record value"""

    def update_room_capacity(self):
        update_val = self.env["hotel.room.type"].browse(
            self.env.context.get("active_ids")
        )
        vals = {"room_capacity": self.room_capacity}
        update_val.write(vals)

    """create the cal_total_capacity method to calculate the total Person for room Capacity """


    def _cal_total_capacity(self):
        for res in self:
            res.update(
                {
                    "room_capacity": res.adult + res.child,
                }
            )

    @api.constrains("adult")
    def check_adult(self):
        for reservation in self:
            if reservation.adult <= 0:
                raise ValidationError("Adults must be more than 0")
