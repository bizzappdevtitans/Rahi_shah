from odoo import fields, models,api
from odoo.exceptions import UserError


class Schoolcourse(models.Model):
    _name = "school.course"
    _description = "School Module"
    _rec_name = "stand"

    # stand = fields.Char(string="Standard")
    stand = fields.Selection(
        [
            ("11thcommerce", "11thCommerce"),
            ("11thscience", "11thScience"),
            ("12thCommerce", "12thCommerce"),
            ("12thscience", "12thScience"),
        ]
    )

    subject_details = fields.Many2many("school.subject", "subject")

    teacher_details = fields.Many2many("school.teacher", string="teacher_Details")

    fees_details=fields.Many2many("school.fees",string="Fees Details")
    teacher_count = fields.Integer(string="teacher_count", compute="compute_count")


    def get_teacher(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Teacher",
            "view_mode": "tree,form",
            "res_model": "school.teacher",
            "domain": [("id", "in", self.teacher_details.ids)],
            "context": "{'create': False}",

        }


    #search Count ORM method 
    def compute_count(self):
        for record in self:
            record.teacher_count = self.env['school.teacher'].search_count(
                [('id', 'in', self.teacher_details.ids)])
    