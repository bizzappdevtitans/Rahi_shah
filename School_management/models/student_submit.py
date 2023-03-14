from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime


class StudentSubmit(models.Model):
    _name = "school.submit"
    _description = "School Module"
    _rec_name = "name_id"

    name_id = fields.Many2one("school.student", "student Name")
    stu_stand = fields.Char(string="Student Standard")
    assi_sub = fields.Char(string="Subject")
    sub = fields.Binary(string="Upload here")
    state = fields.Selection(
        [
            ("start", "Start"),
            ("mode", "In Progrees"),
            ("done", "Done"),
            ("confirm", "Confirm"),
        ],
        string="status",
        required=True,
        readonly=True,
        copy=False,
        default="start",
    )
    deadline_date = fields.Date(string="Deadline Date")

    assin_message = fields.Selection(
        [
            ("notsubmit", "Today is last day for Assignment Submission"),
            ("submit", " "),
        ]
    )
    assignment_details_ids = fields.Many2many("school.assignmnent", "task")
    description = fields.Text()

    def button_in_progress(self):
        self.write({"state": "mode"})  # written the state mode for In progress

    def button_done(self):
        self.write({"state": "done"})  # written the state mode for Done

    def button_confirm(self):
        self.write({"state": "confirm"})  # written the state mode for confirm

    @api.model
    def cron_send_message(self):
        print("Submitted")
        if self.env["school.submit"].search(
            [("deadline_date", "=", fields.Date.today())]
        ):
            self.env["school.submit"].search(
                [("deadline_date", "=", fields.Date.today())]
            ).write({"assin_message": "notsubmit"})

        elif self.env["school.submit"].search(
            [("deadline_date", "!=", fields.Date.today())]
        ):
            self.env["school.submit"].search(
                [("deadline_date", ">=", fields.Date.today())]
            ).write({"assin_message": "submit"})

    """Create the _unlink_except_done function if user delete the record but 
    it's mode is done at that time UserError is occur """

    @api.ondelete(at_uninstall=False)  # Use the Ondelete Method Decorators
    def _unlink_except_done(self):
        if (state == "done" for state in self):
            raise UserError(("You cannot delete,it's in Done Mode....."))
