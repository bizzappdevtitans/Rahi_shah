from odoo import fields, models, api


class HotelAmenity(models.Model):
    _name = "hotel.amenity"
    _description = "Hotel Amenities"

    product_id = fields.Many2one(
        "product.product",
        "Amenities",
        required=True,
        delegate=True,
        ondelete="cascade",
    )
    type_id = fields.Many2one(
        "amenity.types",
        "Amenity Type",
        required=True,
        ondelete="restrict",
    )
    manager_id = fields.Many2one("res.users", string="Manager")


    @api.model
    def create(self, vals):
        if "type_id" in vals:
            prod = self.env["amenity.types"].browse(vals["type_id"])
            vals.update({"categ_id": prod.categ_id.id})
        return super(HotelAmenity, self).create(vals)

    """For adding  string into name while duplicating a record"""

    def copy(self, default=None):

        self.ensure_one()
        if default is None:
            default = {}
        if "name" not in default:
            default["name"] = self.name
        return super(HotelAmenity, self).copy(default=default)
