from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolResult(models.Model):
    _name = "student.result"
    _description = "School Module"
    _rec_name = "name_id"

    result_sequence = fields.Char(
        "Student sequence", index=True, copy=False, default="New"
    )
    name_id = fields.Many2one("school.student", "student Name")
    Email = fields.Char(related="name_id.Email", string="Student Mail")
    roll = fields.Integer(String="RollNumber")
    Eco = fields.Integer(string="Economic")
    ba = fields.Integer(string="business administration")
    acc = fields.Integer(string="Accouting")
    state = fields.Integer(string="Stastical")
    Gujrati = fields.Integer(string="Gujrati")
    total = fields.Integer(string="Total", compute="cal_marks")
    percentage = fields.Float(string="percentage", compute="cal_perce")
    result = fields.Selection(
        [
            ("pass", "PASS"),
            ("fail", "FAIL"),
        ]
    )
    grade = fields.Char("Grade")

    

    @api.depends("Eco", "ba", "acc", "state", "Gujrati")
    def cal_marks(self):
        """Create the cal_marks function to calculate the total Marks
        if Teacher change the Marks  of the student then the total Marks is also change """
        for res in self:
            res.update(
                {
                    "total": res.Eco + res.ba + res.acc + res.state + res.Gujrati,
                }
            )

    
    def cal_perce(self):
        """ create the cal_perce function to calculate the percentage """

        for res in self:
            res.update(
                {
                    "percentage": res.total / 500,
                }
            )

    # Use the SQL Constraints for Roll Number must be unique

    _sql_constraints = [
        ("roll_unique", "unique(roll)", "Roll number Must be  is unique..."),
    ]

    

    @api.constrains("Eco", "ba", "acc", "state", "Gujrati")
    def _check_marks(self):
        """Create the _check_marks function for Checking the Marks is not greater than 100 
        if Teacher Enter the mopre than 100 it will generate the Validation Error"""
        for rec in self:
            if (
                rec.Eco > 100
                or rec.ba > 100
                or rec.acc > 100
                or rec.state > 100
                or rec.Gujrati > 100
            ):
                raise ValidationError("Marks can't be more than 100")

    # generating sequence Student Result

    @api.model
    def create(self, vals):
        if vals.get("result_sequence", ("New")) == ("New"):
            vals["result_sequence"] = self.env["ir.sequence"].next_by_code(
                "student.result"
            )
            res = super(SchoolResult, self).create(vals)
        return res
