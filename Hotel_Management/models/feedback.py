from odoo import api, fields, models


class Feedback(models.Model):

    _name = "hotel.feedback"
    _description = "Feedback"
    _rec_name = "guest_name_id"

    guest_name_id= fields.Many2one("res.partner", string="Guest Name")
    rating = fields.Selection(
        [
            ("poor", "Poor"),
            ("average", "Average"),
            ("good", "Good"),
            ("excellent", "Excellent"),
        ]
    )
    suggestion = fields.Char(string="Suggestion")
