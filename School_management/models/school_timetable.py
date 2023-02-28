from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolTimeTable(models.Model):
    _name = "school.timetable"
    _description = "School Module"
    _rec_name = "lec_sub"

    stand = fields.Char(string="Standard")
    lec_date = fields.Datetime(string="Lecture date and Time")
    lec_sub = fields.Char(string="Lecture Subject")
    name_id = fields.Many2one("school.teacher", "LectureBy")
    phone = fields.Char(related="name_id.phone", string="phone")

    @api.constrains("lec_date")
    def _check_date(self):
        for record in self:
            if record.lec_date < fields.Datetime.today():
                raise ValidationError("The Lecture date cannot be set in the past")
