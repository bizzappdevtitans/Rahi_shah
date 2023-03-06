from odoo import api, fields, models
from odoo.exceptions import UserError


class StudentSubmit(models.Model):
    _name = "school.submit"
    _description = "School Module"
    _rec_name="name_id"

    name_id = fields.Many2one("school.student", "student Name")
    stu_stand = fields.Char(string="Student Standard")
    assi_sub = fields.Char(string="Subject")
    sub = fields.Binary(string="Upload here")
    state = fields.Selection(
        [
            ("start", "Start"),
            ("mode", "In Progrees"),
            ("done", "Done"),
        ],
        string="status",
        required=True,
        readonly=True,
        copy=False,
        default="start",
    )

    def button_in_progress(self):
        self.write({"state": "mode"})

    def button_done(self):
        self.write({"state": "done"})

    assignment_details_ids = fields.Many2many("school.assignmnent", "task")
    description = fields.Text()

#ondelete API method to can't delete the Done Mode Records    

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done(self):
        if (state == "done" for state in self):
            raise UserError(("You cannot delete,it's in Done Mode....."))
