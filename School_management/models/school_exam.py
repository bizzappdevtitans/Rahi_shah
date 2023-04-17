from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class schoolExam(models.Model):
    _name = "school.exam"
    _description = "Exam Schedule"
    _rec_name = "standard"

    standard = fields.Char(string="Standard")
    date = fields.Date(string="Date of Exam")
    day = fields.Char(string="Day of Exam")
    subject = fields.Char(string="Subject")


    @api.constrains("date")
    def _check_date(self):

        """ create the _check_date function for check the Date of Exam
        if Admin select the past Date for Exam then it will generate the Validation Error """
        
        for record in self:
            if record.date < fields.Date.today():
                raise ValidationError("The Exam Date cannot be set in the Past")
