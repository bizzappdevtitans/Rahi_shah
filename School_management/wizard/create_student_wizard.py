from odoo import fields, models


class createstudent(models.TransientModel):
    _name = "create.student.wizard"

    name = fields.Char(string="Student Name")
    Email = fields.Char(string="Student Mail")

    """create the action_create_student function to create Record
    in the student model and after clicking in the button Record is added"""

    def action_create_student(self):
        vals = {"name": self.name, "Email": self.Email}
        self.env["school.student"].create(vals)
