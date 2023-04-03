from odoo import api, fields, models
from odoo.exceptions import ValidationError



class HouseKeepingService(models.Model):

    _name = "house.keeping.service"
    _description = "House Keeping Service"
    _rec_name = "room_no"

    room_no = fields.Char(string="Room No")
    inspect_date = fields.Datetime(string="Inspect Date-Time")
    clean_type = fields.Selection(
        [
            ("daily", "Daily"),
            ("2 day", "2 Days"),
            ("week", "Week"),
        ]
    )
    inspector = fields.Many2one("res.users", string="Inspector")
    house_keeping_ids = fields.Many2many("house.keeping.activity")
    house_keeping_count = fields.Integer(
        string="Booking count", compute="_compute_count"
    )

    # Write the Method to generate the Smart Button

    def get_house_service(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "House Keeping",
            "view_mode": "tree,form",
            "res_model": "house.keeping.activity",
            "domain": [("id", "in", self.house_keeping_ids.ids)],
            "context": "{'create': False}",
        }
     # create the _compute_count method to count the total Records of the smart Button

    def _compute_count(self):
        for record in self:
            record.house_keeping_count = len(self.house_keeping_ids)

    """ create the _check_time method to check the inspect_date
    if user select the Past date it will generate the Validation error"""        

    @api.constrains("inspect_date")
    def _check_time(self):
        if self.inspect_date < fields.Datetime.now():
            raise ValidationError(
                ("Inspect Date Time should be greater than the current Date Time .")
            )  

