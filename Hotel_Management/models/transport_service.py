from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError


class TransportService(models.Model):

    _name = "transport.service"
    _description = "Transport Service"
    _rec_name = "trans_sequence"

    trans_sequence = fields.Char(
        "Reservation No", required=True, index=True, copy=False, default="New"
    )
    pick_up_date = fields.Date(string="Pickup Date")
    guest_name = fields.Many2one("res.partner", string="Guest Name")
    no_adult = fields.Integer(string="Adult")
    no_child = fields.Integer(string="Child")
    phone = fields.Char(string="Contact No")
    pickup_required = fields.Selection(
        [
            ("yes", "YES"),
            ("no", "NO"),
        ]
    )
    pickup_time = fields.Datetime(string="Pickup Time")
    destination = fields.Char(string="Destination")
    pickup_location = fields.Char(string="Pickup Location")
    is_chargable = fields.Boolean(string="Chargable", default=True)
    Trasport_mode = fields.Selection(
        [
            ("innova", "Innova"),
            ("swift", "Swift"),
            ("eeco", "Maruti Suzuki Eeco"),
        ]
    )

    # Generate Sequence

    @api.model
    def create(self, vals):
        if vals.get("trans_sequence", ("New")) == ("New"):
            vals["trans_sequence"] = self.env["ir.sequence"].next_by_code(
                "transport.service"
            )
            record = super(TransportService, self).create(vals)
        return record
        
    """create the action_send_whatsapp function to send the message in whatsapp
    when user click on the button the message will be send """

    def action_send_whatsapp(self):
        if not self.phone:
            raise ValidationError("Missing the Phone Number")
        msg = "Your Transport Service is sucessfully Register %s" % self.guest_name
        print(msg)
        whatsapp_api_url = (
            "https://web.whatsapp.com/send?phone=" + self.phone + "&text=" + msg
        )

        return {
            "type": "ir.actions.act_url",
            "target": "new",
            "url": whatsapp_api_url,
        }

    """Create the _check_dates method to check the pick_up_date
    if User select Past date it will generate the validation Error"""

    @api.constrains("pick_up_date")
    def _check_dates(self):
        if self.pick_up_date < fields.Date.today():
            raise ValidationError(
                ("Pick Up date should be greater than the current date.")
            )

    """Create the _check_time  method to check the pickup_time 
    if User select Past Time it will generate the validation Error"""

    @api.constrains("pickup_time")
    def _check_time(self):
        if self.pickup_time < fields.Datetime.now():
            raise ValidationError(
                ("Pick Up Time should be greater than the current Time.")
            )

    """ create the phone_validation function for check the length of the phone number 
    if user enter characters,less than or more than 10 Numbers it will generate the Validation Error"""

    @api.constrains("phone")
    def phone_validation(self):
        for record in self:
            if len(record.phone) != 10 or record.phone.isdigit() == False:
                raise ValidationError("Phone Number is not valid")
