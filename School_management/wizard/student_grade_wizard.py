from odoo import models, fields


class StudentWizard(models.TransientModel):
    _name = "student.grade.wizard"

    def _get_default_students(self):
        return self.env["school.student"].browse(self.env.context.get("active_ids"))

    student_ids = fields.Many2many(
        "school.student", string="Student", default=_get_default_students
    )
    grade = fields.Char("Grade")

    """create the set_student_grade function to set the value for garde field 
    when Add the grade and click on button after that grade field value is filled out"""

    def set_student_grade(self):
        for record in self:
            if record.student_ids:
                for student in record.student_ids:
                    student.grade = self.grade

    """create the action_update_student_grade function to Update the Record value"""

    def action_update_student_grade(self):
        update_val = self.env["school.student"].browse(
            self.env.context.get("active_ids")
        )
        vals = {"grade": self.grade}
        update_val.write(vals)
