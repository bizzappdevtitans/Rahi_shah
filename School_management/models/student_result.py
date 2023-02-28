from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolResult(models.Model):
    _name = "student.result"
    _description = "School Module"

    result_sequence = fields.Char(
        "Student sequence", required=True, index=True, copy=False, default="New"
    )
    name = fields.Many2one("school.student", "student Name")
    Email = fields.Char(related="name.Email", string="Student Mail")
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

    @api.depends("Eco", "ba", "acc", "state", "Gujrati")
    def cal_marks(self):
        for res in self:
            res.update(
                {
                    "total": res.Eco + res.ba + res.acc + res.state + res.Gujrati,
                }
            )

    def cal_perce(self):
        for res in self:
            res.update(
                {
                    "percentage": res.total / 500,
                }
            )

    _sql_constraints = [
        ("roll_unique", "unique(roll)", "Roll number Must be  is unique..."),
    ]

    @api.constrains("Eco", "ba", "acc", "state", "Gujrati")
    def _check_date(self):
        for rec in self:
            if (
                rec.Eco > 100
                or rec.ba > 100
                or rec.acc > 100
                or rec.state > 100
                or rec.Gujrati > 100
            ):
                raise ValidationError("Marks can't be more than 100")

    # generetaing sequence

    @api.model
    def create(self, vals):
        if vals.get("result_sequence", ("New")) == ("New"):
            vals["result_sequence"] = self.env["ir.sequence"].next_by_code(
                "student.result"
            )
            res = super(SchoolResult, self).create(vals)
        return res




