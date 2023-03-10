from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolAssignment(models.Model):
    _name = "school.assignmnent"
    _description = "School Module"
    _rec_name = "subject"

    standard = fields.Char(string="Standard")
    subject = fields.Char(string="Subject")
    task = fields.Char(string="Describe assignmnent")
    submit = fields.Datetime(string="Deadline Time")

    """ create the _check_date function for check the Deadline Date
    if user select the past Date for Deadline then it will generate the Validation Error """

    @api.constrains("submit")  # use the constrains method decorators
    def _check_date(self):
        for record in self:
            if record.submit < fields.Datetime.today():
                raise ValidationError("The Deadline Time cannot be set in the Past")
