from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LaundryService(models.Model):

    _name = "laundry.service"
    _description = "Laundry Service"
    _rec_name = "order_reference"

    order_reference = fields.Char(
        "Order No", required=True, index=True, copy=False, default="New"
    )
    request_date = fields.Date(string="Request Date")
    request_deadline = fields.Date(string="Request Deadline")
    shop_name_id = fields.Many2one("res.company", string="Shop Name")
    room_no = fields.Char(string="Room No")
    guest_name = fields.Many2one("res.partner", string="Guest Name")
    laundry_list_ids = fields.Many2many(
        "laundry.service.line", string="Laundry Service"
    )
    laundry_service_count = fields.Integer(
        string="Booking count", compute="_compute_count"
    )

    # Write the Method to generate the Smart Button

    def get_laundry_service(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "laundry",
            "view_mode": "tree,form",
            "res_model": "laundry.service.line",
            "domain": [("id", "in", self.laundry_list_ids.ids)],
            "context": "{'create': False}",
        }
     # create the _compute_count method to count the total Records of the smart Button
     
    def _compute_count(self):
        for record in self:
            record.laundry_service_count = len(self.laundry_list_ids)


    # Generate Sequence

    @api.model
    def create(self, vals):
        if vals.get("order_reference", ("New")) == ("New"):
            vals["order_reference"] = self.env["ir.sequence"].next_by_code(
                "laundry.service"
            )
            record = super(LaundryService, self).create(vals)
        return record

  

    @api.constrains("request_date","request_deadline")
    def _check_dates(self):
        """Create the _check_dates method to check the Request_date  and request_deadline 
        if user select past date  it will generate the Validation error """
        if self.request_date < fields.Date.today():
            raise ValidationError(
                ("Date should be greater than the current date.")
            )

        if self.request_deadline <= self.request_date:
            raise ValidationError(
                ("Deadline Date should be Graeter Than!")
            )
