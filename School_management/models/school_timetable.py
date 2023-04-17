from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolTimeTable(models.Model):
    _name = "school.timetable"
    _description = "School Module"
    _rec_name = "lec_sub"

    stand = fields.Char(string="Standard")
    lec_date = fields.Datetime(string="Lecture date and Time")
    lec_sub = fields.Char(string="Lecture Subject")
    name_id = fields.Many2one("school.teacher", "LectureBy")
    phone = fields.Char(related="name_id.phone", string="phone")

   
    @api.constrains("lec_date")
    def _check_date(self):
        """create the _check_date function for check the Date of Lecture
        if Admin select the past Date for Lecture then it will generate the Validation Error """

        for record in self:
            if record.lec_date < fields.Datetime.today():
                raise ValidationError("The Lecture date cannot be set in the past")

   
    def action_send_whatsapp(self):

        """create the action_send_whatsapp function to send the message in whatsapp
        when user click on the button the message will be send """

        if not self.name_id.phone:
            raise ValidationError("Missing the Phone Number")
        msg = "Today is Lecture %s" % self.name_id.name
        whatsapp_api_url = (
            "https://web.whatsapp.com/send?phone=" + self.phone + "&text=" + msg
        )

        return {
            "type": "ir.actions.act_url",
            "target": "new",
            "url": whatsapp_api_url,
        }
