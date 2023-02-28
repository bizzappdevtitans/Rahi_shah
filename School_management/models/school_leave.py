from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolLeave(models.Model):
    _name = "school.leave"
    # _inherit = "school.teacher"
    _description = "School Module"

    name = fields.Many2one("school.teacher", "Teacher")
    reason = fields.Char(string="Reason")
    date = fields.Date(string="Leave Date")
    mode = fields.Selection(
        [
            ("half", "HalfLeave"),
            ("full", "FullLeave"),
        ]
    )

    @api.constrains("date")
    def _check_date(self):
        for record in self:
            if record.date < fields.Date.today():
                raise ValidationError("The Leave date cannot be set in the Past")
