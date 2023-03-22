from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentAttendance(models.Model):
    _name = "student.attendance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Attendance Module"
    _rec_name = "name_id"

    date = fields.Date(string="Today's Date")
    standard = fields.Selection(
        [
            ("11", "11th Standard"),
            ("12", "12th Standard"),
        ]
    )
    name_id = fields.Many2one("school.student", "student Name")
    Email = fields.Char(related="name_id.Email", string="Student Mail")
    attendance = fields.Selection(
        [
            ("present", "Present"),
            ("absent", "Absent"),
        ]
    )

    """create the _check_date function for check the Date of Attendance
    if Admin select the Future Date for Attendance then it will generate the Validation Error """

    @api.constrains("date")
    def _check_date(self):
        for record in self:
            if record.date > fields.Date.today():
                raise ValidationError("The Attendance Date cannot be set in the Future")
