from odoo import fields, models


class Schoolsubject(models.Model):
    _name = "school.subject"
    _description = "School Module"
    _rec_name = "stand"

    stand = fields.Selection(
        [
            ("11thcommerce", "11thCommerce"),
            ("11thscience", "11thScience"),
            ("12thCommerce", "12thCommerce"),
            ("12thscience", "12thScience"),
        ]
    )

    sub_name = fields.Char(string="Subject Name")
    sub_type = fields.Selection(
        [
            ("compulsory", "compulsory"),
            ("elective", "Elective"),
        ]
    )
    co_type = fields.Selection(
        [
            ("theory", "Theory"),
            ("pratical", "Pratical"),
        ]
    )
