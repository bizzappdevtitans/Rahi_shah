from odoo import api, fields, models


class LaundryServiceLine(models.Model):

    _name = "laundry.service.line"
    _description = "Laundry Service"
    _rec_name="service_name"


    service_name = fields.Selection(
        [
            ("washing_clothes", "Washing Clothes"),
            ("roll_press", "Roll Press"),
            ("iron","Iron")
        ]
    )
    cost_rate=fields.Float(string="Cost Rate")
    qty=fields.Integer(string="Quantity")
    total_cost=fields.Integer(string="Total Cost" , compute="cal_total_cost")

    """create the cal_total_cost method to count the total price"""
    @api.onchange("cost_rate", "qty")
    def cal_total_cost(self):
        for res in self:
            res.update(
                {
                    "total_cost": res.cost_rate * res.qty,
                }
            )