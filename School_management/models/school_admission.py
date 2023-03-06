from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
import re


class SchoolAdmission(models.Model):
    _name = "school.admission"
    _inherit = ["mail.thread"]
    _description = "School Admission Model"

    admission_id = fields.Char(string="ID")
    sch_name = fields.Char(string="School Name")
    standard = fields.Selection(
        [
            ("11", "11th Standard"),
            ("12", "12th Standard"),
        ]
    )
    field = fields.Selection(
        [
            ("commerce", "Commerce"),
            ("science", "Science"),
        ]
    )
    name = fields.Char(string="Name")
    stu_email = fields.Char(string="Email")
    Gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "FeMale"),
        ]
    )
    birthday = fields.Date(string="BirthDate")
    Age = fields.Char(string="Student Age")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Contact")
    admission_query = fields.Text()
    admission_count = fields.Integer(compute="damage")
    desc = fields.Text()

    admision_state = fields.Selection(
        [
            ("start", "Start"),
            ("mode", "In Progrees"),
            ("confirm", "Confirm"),
        ],
        string="status",
        required=True,
        readonly=True,
        copy=False,
        default="start",
    )

    def button_in_progress(self):
        self.write({"admision_state": "mode"})

    def button_confirm(self):
        self.write({"admision_state": "confirm"})

    """Apply the API Constarints for the name must be filledout validation """

    @api.constrains("name")
    def _name_validation(self):
        for record in self:
            if record.name == False:
                raise ValidationError("Name must be filled out")

    # the API Constraints for the name length validation
    @api.constrains("name")
    def name_validate(self):
        for record in self:
            if len(record.name) < 2:
                raise ValidationError("Length of Name is not valid...")

    # the API Constraints for the user can't select the Future date

    @api.constrains("birthday")
    def _check_date(self):
        for record in self:
            if record.birthday > fields.Date.today():
                raise ValidationError("The BirthDate cannot be set in the Future")

    #  the API Constraints for the phone number validation can't be more than 10
    @api.constrains("phone")
    def phone_validation(self):
        for record in self:
            if len(record.phone) != 10:
                raise ValidationError("Phone Number is not valid")

    # the API Constraints for the user Email validation
    @api.constrains("stu_email")
    def validate_mail(self):
        if self.stu_email:
            match = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-a0-9-]+)*(\.[a-z]{2,4})$",
                self.stu_email,
            )
            if match == None:
                raise ValidationError("Email id is not valid")

    # browse ORM Method to print the record

    @api.depends("admission_id")
    def action_browse(self):
        for rec in self:
            rec.desc = self.env["school.admission"].browse(rec.admission_id).name
            return self.desc

    # Default_Get ORM Method for print the default value
    def default_get(self, field_list=[]):
        retur = super(SchoolAdmission, self).default_get(field_list)
        retur["name"] = "Your Name"
        return retur

    # unlink ORM Method for can't delete the confirm admission

    @api.model
    def unlink_method(self, values):
        if (admision_state == "confirm" for admision_state in self):
            raise UserError(("You cannot delete,it's in Confirm Mode....."))
        unlink_record = super(SchoolAdmission, self).unlink()
        return unlink_record
