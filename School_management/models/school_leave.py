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
    
    @api.constrains("date")  #use constrains Method Decoratos
    def _check_date(self):
        
        """ create the _check_date function for check the Date of Leave
        if Teacher select the past Date for Leave then it will generate the Validation Error """
    
        for record in self:
            if record.date < fields.Date.today():
                raise ValidationError("The Leave date cannot be set in the Past")
