from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolLeave(models.Model):
    _name = "school.leave"
    _description = "School Module"
    _rec_name = "name_id"

    name_id = fields.Many2one("school.teacher", "Teacher")
    reason = fields.Char(string="Reason")
    date = fields.Date(string="Leave Date")
    mode = fields.Selection(
        [
            ("half", "HalfLeave"),
            ("full", "FullLeave"),
        ]
    )
    
    # apply thr API Constraints for the user can't select the past date
    @api.constrains("date")
    def _check_date(self):
        for record in self:
            if record.date < fields.Date.today():
                raise ValidationError("The Leave date cannot be set in the Past")
