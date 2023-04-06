from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HouseKeepingactivity(models.Model):

    _name = "house.keeping.activity"
    _description = "House Keeping Activity"
    _rec_name = "house_keeping_activity"

    house_keeping_activity = fields.Selection(
        [
            ("cleaning floor", "Cleaning Floor"),
            ("change of curtains", "Change of Curtains"),
            ("dusting", "Dusting"),
        ]
    )
    house_keeper = fields.Char(string="House Keeper")
    clean_start = fields.Datetime(string="Clean Start Time")
    clean_end = fields.Datetime(string="Clean End Time")
    dirty = fields.Boolean(string="Dirty")
    clean = fields.Boolean(string="Clean")

    
    @api.constrains("clean_start","clean_end")
    def _check_dates_times(self):
        """Create the _check_dates_times method to check the clean_start and clean_end 
        if user select past date and time it will generate the Validation error """
    
        if self.clean_start < fields.Datetime.now():
            raise ValidationError(
                ("Cleaning  Time should be greater than the current Time.")
            )  
        if self.clean_end <= self.clean_start:
            raise ValidationError(
                ("Date and Time should be Graeter Than!")
            )

