from odoo import api, fields, models


class FeesStatus(models.Model):
    _name = "fees.status"
    _inherit = "school.fees"

    fee_status = fields.Selection(
        [
            ("pending", "Pending"),
            ("complete", "Complete"),
        ]
    )
    name = fields.Many2one("school.student", "student Name")