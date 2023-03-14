from odoo import api, fields, models


class Schoolfees(models.Model):
    _name = "school.fees"
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

    academic_fees = fields.Integer(string="Admission Fees")
    tuition_fees = fields.Integer(string="Tuition Fees")
    sports_fees = fields.Integer(string="Sports Charge")
    exam_fees = fields.Integer(string="Exam Fees")
    total_fees = fields.Integer(string="Total Fees")

    """Create the cal_fees function to calculate the total fees
    if Admin chage the Amount of the fees then the total fees amount is also change """

    @api.onchange("academic_fees", "tuition_fees", "sports_fees", "exam_fees")  # Onchange method for count the total Fees 
    def cal_fees(self):
        for res in self:
            res.update(
                {
                    "total_fees": res.academic_fees
                    + res.tuition_fees
                    + res.sports_fees
                    + res.exam_fees,
                }
            )
