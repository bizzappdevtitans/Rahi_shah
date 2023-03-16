import datetime
from datetime import date
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import re


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "School Module"

    sequence = fields.Char(
        "Student Reference", required=True, index=True, copy=False, default="New"
    )
    name = fields.Char(string="Student Name", required=True)
    Email = fields.Char(string="Student Mail")
    birth = fields.Date(string="BirthDate")
    Gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "FeMale"),
            ("other", "Other"),
        ]
    )
    Age = fields.Char(string="Student Age", tracking=True)
    address = fields.Text(string="Address")
    Hobby = fields.Char(string="Hobby")
    result = fields.Float(string="Enter last year Result")
    city = fields.Boolean(string="Click if you from ahmedabad")
    photo = fields.Binary(string="student Photo")
    grade = fields.Char("Grade")
    query = fields.Text()
    birthday_wish = fields.Selection(
        [
            ("wish", "Happy birthday"),
            ("later", " "),
        ]
    )

    result_list_ids = fields.Many2many("student.result", string="student_result")
    result_count = fields.Integer(string="result_count", compute="_compute_count")

    # Write the Method to generate the Smart Button

    def get_result(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Teacher",
            "view_mode": "tree,form",
            "res_model": "student.result",
            "domain": [("id", "in", self.result_list_ids.ids)],
            "context": "{'create': False}",
        }

    # create the _compute_count method to count the total Records of the smart Button

    def _compute_count(self):
        for record in self:
            record.result_count = len(self.result_list_ids)

    """Create the _calc_age function to calculate the Age of the student based on the 
    today date if student change the date then age of student is also change """

    @api.onchange("birth")
    def _calc_age(self):
        for res in self:
            today = date.today()
            if res.birth:
                res.Age = today.year - res.birth.year

    """ create the _unlink_except_done function for not deleteing the particular Record
    if User try to delete zaid Record then it will generate the User Error """

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done(self):
        if self.name == "zaid":
            raise UserError(("You cannot delete...."))

    """ Create the validate_mail function for validate the User eamil id pattern """

    @api.constrains("Email")
    def validate_mail(self):
        if self.Email:
            match = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                self.Email,
            )
            if match == None:
                raise ValidationError("Email id is not valid")

    # Generating Sequence

    @api.model
    def create(self, vals):
        if vals.get("sequence", ("New")) == ("New"):
            vals["sequence"] = self.env["ir.sequence"].next_by_code("school.student")
            res = super(SchoolStudent, self).create(vals)
        return res

    # Create the Name search ORM method to search the Name

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("name", operator, name),
                ("Email", operator, name),
            ]

        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
        return super(SchoolStudent, self)._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )

    """create the _cron_send_birthday method for print the birthday message,
    DOB compare with today's date if the date is match it will print the birthday message 
    this method link with cron job """

    @api.model
    def _cron_send_birthday(self):
        print("birthday")
        if self.env["school.student"].search([("birth", "=", fields.Date.today())]):
            self.env["school.student"].search(
                [("birth", "=", fields.Date.today())]
            ).write({"birthday_wish": "wish"})

        elif self.env["school.student"].search([("birth", "!=", fields.Date.today())]):
            self.env["school.student"].search(
                [("birth", "!=", fields.Date.today())]
            ).write({"birthday_wish": "later"})

    """create the action_send_birthday_email method to send the birthday mail using 
    cron job """

    def action_send_birthday_email(self):
        for record in self.search([]):
            today = date.today()
            print(today)
            if today.day == record.birth.day and today.month == record.birth.month:
                template_id = self.env.ref(
                    "School_management.student_birthday_mail_template"
                ).id
                template = self.env["mail.template"].browse(template_id)
                template.send_mail(record.id, force_send=True)
                message = "Happy Birthday"
                channel_id = self.env.ref("mail.channel_all_employees").id
                channel = self.env["mail.channel"].browse(channel_id)
                channel.message_post(
                    body=(message),
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )
