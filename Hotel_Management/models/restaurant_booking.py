from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RestaurantBooking(models.Model):

    _name = "restaurant.booking"
    _description = "Restaurant Booking"
    _rec_name = "booking_no"

    booking_no = fields.Char(
        "Booking No", required=True, index=True, copy=False, default="New"
    )
    guest_name = fields.Many2one("res.partner", string="Guest Name")
    booking_date = fields.Datetime(string="Date")
    room_no = fields.Char(string="Room No")
    table_booking_list_ids = fields.Many2many("table.booking")
    food_servive_ids = fields.Many2many("food.service")

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirm"),
            ("cancel", "Cancel"),
        ],
        string="status",
        required=True,
        readonly=True,
        copy=False,
        default="draft",
    )
    
    def button_confirm(self):
        self.write({"state": "confirm"})  # written the state mode for Confirm

    def button_cancel(self):
        self.write({"state": "cancel"})  # written the state mode for Cancel

    # Generate Sequence

    @api.model
    def create(self, vals):
        if vals.get("booking_no", ("New")) == ("New"):
            vals["booking_no"] = self.env["ir.sequence"].next_by_code(
                "restaurant.booking"
            )
            record = super(RestaurantBooking, self).create(vals)
        return record

    @api.constrains("booking_date")
    def _check_dates_times(self):
        if self.booking_date < fields.Datetime.now():
            raise ValidationError(
                ("Booking Date should be greater than the current Date Time.")
            ) 
