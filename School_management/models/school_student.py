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
    query = fields.Text()

    result_list = fields.Many2many("student.result", string="student_result")
    result_count = fields.Integer(string="result_count", compute="_compute_count")

    def get_result(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Teacher",
            "view_mode": "tree,form",
            "res_model": "student.result",
            "domain": [("id", "in", self.result_list.ids)],
            "context": "{'create': False}",
        }

    def _compute_count(self):
        for record in self:
            record.result_count = len(self.result_list)

    @api.onchange("birth")
    def _calc_age(self):
        for res in self:
            today = date.today()
            if res.birth:
                res.Age = today.year - res.birth.year

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done(self):
        if self.name == "zaid":
            raise UserError(("You cannot delete...."))

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

    # name search ORM method
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

