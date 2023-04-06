from odoo import fields, models, api
from odoo.exceptions import ValidationError

class AmenityTypes(models.Model):
    _name = "amenity.types"
    _description = "Amenity Types"

    amenity_type_id = fields.Many2one("amenity.types", "Types")
    categ_id = fields.Many2one(
        "product.category",
        "Product Category",
        delegate=True,
        copy=False,
        ondelete="cascade",
    )

    def unlink(self):
        rec = self.env["product.category"].sudo().browse(self.categ_id.id)
        rec.unlink()
        return super(AmenityTypes, self).unlink() 

    """For adding '(copy)' string into name while duplicating a record"""

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "name" not in default:
            default["name"] = self.name
        return super(AmenityTypes, self).copy(default=default)
