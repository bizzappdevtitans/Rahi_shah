from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Module"

    name = fields.Char(string="Name")
    lname = fields.Char(string="last Name")
    phone = fields.Char(string="Contact")
    photo = fields.Binary(string="Upload photo")
    timetable_ids = fields.One2many("school.timetable", "name_id", string="Timetable")
    refernce = fields.Reference(
        selection=[
            ("school.student", "Student profile"),
            ("school.submit", "Submission"),
        ],
        string="Student Details",
    )
    """ create the phone_validate function for check the length of the phon number
    if user enter less than or more than 10 Numbers it will generate the Validation Error"""

    @api.constrains("phone")
    def phone_validation(self):
        for record in self:
            if len(record.phone) != 10:
                raise ValidationError("Phone Number is not valid")

    # create Name_Get ORM Method To Append the First name and last name of teacher

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s %s" % (rec.name, rec.lname)))
        return result
