from datetime import datetime, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class schoolBookIssue(models.Model):
    _name = "school.bookissue"
    _description = "Student BookIssue Module"
    _rec_name = "book_name"

    book_name = fields.Char(string="Book Name")
    card_no = fields.Char(string="Card Number")

    teacher_name_id = fields.Many2one("school.teacher", "Teacher Name")
    stu_name_id = fields.Many2one("school.student", "student Name")
    Email = fields.Char(related="stu_name_id.Email", string="Student Mail")

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

    """ create the _check_date function for check the book Issue date
    if user select the Past Date for issue date then it will generate the Validation Error """

    @api.constrains("issue_date")  # use the Constrains method decorators
    def _check_date(self):
        for record in self:
            if record.issue_date < fields.Date.today():
                raise ValidationError("The Issue date cannot be set in the Past")

    """Create the action_notification function to display the notification message
    when user click on the button"""
    def action_notification(self):
        message = "Button click Successfull"
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": message,
                "type": "success",
                "sticky": False,
            },
        }
