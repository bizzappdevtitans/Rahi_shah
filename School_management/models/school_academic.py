from datetime import datetime
from odoo import fields, models


class Holidays(models.Model):
    _name = "school.academic"
    _description = "public Holidays"

    name = fields.Char(string="Holiday name")
    date = fields.Date(string="date of Holiday")
    day = fields.Char(string="Day")
