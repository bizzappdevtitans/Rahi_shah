from odoo import  fields, models


class RoomFloor(models.Model):
    _name = "room.floor"
    _rec_name = "floor_name"

    floor_name = fields.Char("Floor Name")
    sequence = fields.Integer("sequence")