from odoo import api, fields, models


class FoodService(models.Model):

    _name = "food.service"
    _description = "Food Service"
    _rec_name = "item_name"

    food_sequence = fields.Char(
        "Food Reference", required=True, index=True, copy=False, default="New"
    )
    item_name = fields.Char(string="Item Name")
    food_qty = fields.Integer(string="Quantity")
    price = fields.Float(string="Price")
    sub_total = fields.Float(string="Subtotal", compute="_cal_total_cost")

    # Generate Sequence

    @api.model
    def create(self, vals):
        if vals.get("food_sequence", ("New")) == ("New"):
            vals["food_sequence"] = self.env["ir.sequence"].next_by_code("food.service")
            record = super(FoodService, self).create(vals)
        return record

   
    def _cal_total_cost(self): 
        """create the cal_total_cost method to calculate the total price """
        for res in self:
            res.update(
                {
                    "sub_total": res.food_qty * res.price,
                }
            )
