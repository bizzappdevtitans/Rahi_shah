from odoo import api, fields, models
from datetime import datetime, date
from odoo.exceptions import ValidationError
import re


class RoomReservation(models.Model):

    _name = "room.reservation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Room Reservation"
    _rec_name = "room_booking"

    room_booking = fields.Char(
        "Booking Reference", required=True, index=True, copy=False, default="New"
    )
    guest_name = fields.Many2one("res.partner", string="Guest Name")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "FeMale"),
            ("other", "Other"),
        ]
    )

    address = fields.Text(string="Address")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Contact",required="True")
    check_in = fields.Date(string="Check In Date")
    check_out = fields.Date(string="Check Out Date")
    stay = fields.Integer(string="Staying")
    num_person = fields.Integer(string="Number of Persons", default=1)
    room_type_ids = fields.Many2many("hotel.room.type", string="Room Reservation")
    room_count = fields.Integer(string="Booking count", compute="compute_count")
    sale_order_id = fields.Many2one("sale.order", "sale Order")
    hotel_invoice_id = fields.Many2one("account.move", "Invoice", copy=False)
    trasport_service_ids = fields.Many2many("transport.service")
    laundry_service_ids = fields.Many2many("laundry.service.line")
    room_amenity_ids = fields.Many2many("hotel.amenity")
    identity_proof = fields.Binary(string="Indentity proof", required="True")

    reservation_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Done"),
            ("confirm", "Confirm"),
            ("cancel", "Cancel"),
        ],
        string="status",
        required=True,
        readonly=True,
        copy=False,
        default="draft",
    )

    # Method to generate the Smart Button

    def get_reservation(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Booking",
            "view_mode": "tree,form",
            "res_model": "hotel.room.type",
            "domain": [("id", "in", self.room_type_ids.ids)],
            "context": "{'create': False}",
        }

    # create the compute_count method to count the total Records of the smart Button

    def compute_count(self):
        for record in self:
            record.room_count = self.env[
                "hotel.room.type"
            ].search_count(  # use the Search_count to count the Records
                [("id", "in", self.room_type_ids.ids)]
            )

    def button_done(self):
        self.write({"reservation_state": "done"})  # written the state mode for Confirm

    def button_confirm(self):
        self.write(
            {"reservation_state": "confirm"})  # written the state mode for Confirm
        message = "Booking Successfull"        # Message notification
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": message,
                "type": "success",
                "sticky": False,
            },
        }  
    def button_cancel(self):
        self.write({"reservation_state": "cancel"})  # written the state mode for Cancel

    """Method to generate sequence """

    @api.model
    def create(self, vals):
        if vals.get("room_booking", ("New")) == ("New"):
            vals["room_booking"] = self.env["ir.sequence"].next_by_code(
                "room.reservation"
            )
            record = super(RoomReservation, self).create(vals)
        return record

    """create the _compaute_days method to count the days based on check_in 
    check_out date"""

    @api.onchange("check_in", "check_out")
    def _compute_days(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                fmt = "%Y-%m-%d"
                date_difference = rec.check_out - rec.check_in
                float_days = (
                    date_difference.days + float(date_difference.seconds) / 86400
                )
                self.stay = float_days

    """Create the unlink_method function if user delete the record but 
    the  mode is Confirm  at that time Validation is occur """

    def unlink(self):
        for reserv_rec in self:
            if reserv_rec.reservation_state == "confirm":
                raise ValidationError(
                    "You cannot delete Reservation in confirm  state."
                )
        return super(RoomReservation, self).unlink()

    """create the action_send_booking_email method to send the  mail using 
    cron job """

    def action_send_booking_email(self):
        for record in self.search([]):
            today = date.today()
            template_id = self.env.ref("Hotel_Management.room_booking_mail_template").id
            template = self.env["mail.template"].browse(template_id)
            template.send_mail(record.id, force_send=True)

    """create the action_send_report method to send the mail with the Report Attachment using 
    cron job """

    def action_send_report(self):
        print("send")
        template_report_id = self.env.ref(
            "Hotel_Management.room_report_mail_template"
        ).id
        self.env["mail.template"].browse(template_report_id).send_mail(
            self.id, force_send=True
        )

    """create the validate_mail method to validate the Mail id pattern
    if user enter wrong mail pattern it will raise validation error """

    @api.constrains("email")
    def validate_mail(self):
        if self.email:
            match = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                self.email,
            )
            if match == None:
                raise ValidationError("Email id is not valid")


    """ create the _check_dates function for check the Check In and Check Out date
    if user select the Past Date for Chcek In then it will generate the Validation Error 
    and aslo check the check_out date if check out date is less than check in it generate the error  """

    @api.constrains("check_in", "check_out")
    def _check_dates(self):
        if self.check_in >= self.check_out:
            raise ValidationError(
                ("Check In Date Should be less than the Check Out Date!")
            )

        if self.check_in < fields.Date.today():
            raise ValidationError(
                "check in date should be greater than the current date."
            )

    """create the default_get ORM method to print the default value in the Adult field"""

    def default_get(self, field_list=[]):  # use the Default get ORM Method
        retur = super(RoomReservation, self).default_get(field_list)
        retur["num_person"] = "1"
        return retur


    """ create the phone_validation function for check the length of the phone number 
    if user enter characters,less than or more than 10 Numbers it will generate the Validation Error"""

    @api.constrains("phone")
    def phone_validation(self):
        for record in self:
            if len(record.phone) != 10 or record.phone.isdigit() == False:
                raise ValidationError("Phone Number is not valid")
