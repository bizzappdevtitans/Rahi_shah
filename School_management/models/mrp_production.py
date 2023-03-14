from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    Manufacturing_desc = fields.Char(string="Manufacturing")
