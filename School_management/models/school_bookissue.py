from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class schoolBookIssue(models.Model):
    _name = "school.bookissue"
    _description = "Student BookIssue Module"
    _rec_name = "book_name"

    book_name = fields.Char(string="Book Name")
    card_no = fields.Char(string="Card Number")

    teacher_name = fields.Many2one("school.teacher", "Teacher Name")
    stu_name = fields.Many2one("school.student", "student Name")
    Email = fields.Char(related="stu_name.Email", string="Student Mail")

    stand = fields.Selection(
        [
            ("11thcommerce", "11thCommerce"),
            ("11thscience", "11thScience"),
            ("12thCommerce", "12thCommerce"),
            ("12thscience", "12thScience"),
        ]
    )
    issue_date = fields.Date(string="Book Issue Date")
    return_date = fields.Date(string="Book Return Date")

    @api.constrains("issue_date")
    def _check_date(self):
        for record in self:
            if record.issue_date < fields.Date.today():
                raise ValidationError("The Issue date cannot be set in the Past")

    @api.model
    def create(self, value):
        value = {"book_name": "ABC"}
        name_create = super(schoolBookIssue, self).create(value)
        return name_create
