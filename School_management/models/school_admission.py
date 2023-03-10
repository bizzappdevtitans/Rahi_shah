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
        self.write({"admision_state": "mode"})  # written the state mode for In progress

    def button_confirm(self):
        self.write({"admision_state": "confirm"})  # written the state mode for Confirm

    """Create the _name_validation function for validate the Name field must be filled out
    if name field is empty then it will generate the Validation Error"""

    @api.constrains("name")  # use the constrains method decorators
    def _name_validation(self):
        for record in self:
            if record.name == False:
                raise ValidationError("Name must be filled out")

    """Create the name_validate function for validate the Name length
    if User Enter less than 2 character in Name then it will Generate the Validation Error """

    @api.constrains("name")  # use the constrains method decorators
    def name_validate(self):
        for record in self:
            if len(record.name) < 2:
                raise ValidationError("Length of Name is not valid...")

    """ create the _check_date function for check the Birthdate
    if user select the future Date for birthday then it will generate the Validation Error """

    @api.constrains("birthday")  # use the constrains method decorators
    def _check_date(self):
        for record in self:
            if record.birthday > fields.Date.today():
                raise ValidationError("The BirthDate cannot be set in the Future")

    """ create the phone_validate function for check the length of the phon number
    if user enter less than or more than 10 Numbers it will generate the Validation Error"""

    @api.constrains("phone")  # use the constrains method decorators
    def phone_validation(self):
        for record in self:
            if len(record.phone) != 10:
                raise ValidationError("Phone Number is not valid")

    """ Create the validate_mail function for validate the User eamil id pattern """

    @api.constrains("stu_email")  # use the constrains method decorators
    def validate_mail(self):
        if self.stu_email:
            match = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-a0-9-]+)*(\.[a-z]{2,4})$",
                self.stu_email,
            )
            if match == None:
                raise ValidationError("Email id is not valid")

    """ create the action_browse method for displaying the record,user click on the browse 
    button in the desc field it's show the user admission id """

    @api.depends("admission_id")  # use the Depends method decorators
    def action_browse(self):
        for rec in self:
            rec.desc = self.env["school.admission"].browse(rec.admission_id).id
            return self.desc

    """create the default_get ORM method to print the default value in the Name field"""

    def default_get(self, field_list=[]):  # use the Default get ORM Method
        retur = super(SchoolAdmission, self).default_get(field_list)
        retur["name"] = "Your Name"
        return retur

    """Create the unlink_method function if user delete the record but 
    it's  admission mode is Confirm  at that time UserError is occur """

    @api.model
    def unlink_method(self, values):  # use the Unlink ORM Method
        if (admision_state == "confirm" for admision_state in self):
            raise UserError(("You cannot delete,it's in Confirm Mode....."))
        unlink_record = super(SchoolAdmission, self).unlink()
        return unlink_record
