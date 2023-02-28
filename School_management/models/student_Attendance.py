from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentAttendance(models.Model):
    _name = "student.attendance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Attendance Module"

    date = fields.Date(string="Today's Date")
    standard = fields.Selection(
        [
            ("11", "11th Standard"),
            ("12", "12th Standard"),
        ]
    )
    name = fields.Many2one("school.student", "student Name")
    Email = fields.Char(related="name.Email", string="Student Mail")
    attendance = fields.Selection(
        [
            ("present", "Present"),
            ("absent", "Absent"),
        ]
    )

    @api.constrains("date")
    def _check_date(self):
        for record in self:
            if record.date > fields.Date.today():
                raise ValidationError("The Attendance Date cannot be set in the Future")



