from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Module"

    name = fields.Char(string="Name")
    lname = fields.Char(string="last Name")
    phone = fields.Char(string="Contact")
    photo = fields.Binary(string="Upload photo")
    timetable = fields.One2many("school.timetable", "name_id", string="Timetable")
    refernce = fields.Reference(
        selection=[
            ("school.student", "Student profile"),
            ("school.submit", "Submission"),
        ],
        string="Student Details",
    )

    @api.constrains("phone")
    def phone_validation(self):
        for record in self:
            if len(record.phone) != 10:
                raise ValidationError("Phone Number is not valid")

    # Name_Get ORM Method

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s %s" % (rec.name, rec.lname)))
        return result

    # browse ORM Method
    def action_browse(self):
        for rec in self:
            teacher = self.env["school.teacher"].browse(9)
            print(teacher.name)