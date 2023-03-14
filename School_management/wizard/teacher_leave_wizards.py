from odoo import api, fields, models


class TeacherLeaveWizard(models.TransientModel):
    _name = "teacher.leave.wizard"
    _description = "Teacher Leave"


def _get_default_students(self):
    return self.env["school.teacher"].browse(self.env.context.get("active_ids"))

    teacher_id = fields.Many2one("school.teacher", string="Teacher", readonly=True)
    date = fields.Date(string="Date")
    reason = fields.Char(string="Reason")

    @api.multi
    def set_teacher(self):
        for record in self:
            if record.teacher_id:
                for teacher in record.teacher_id:
                    teacher.reason = self.reason
