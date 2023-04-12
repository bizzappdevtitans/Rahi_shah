from odoo import fields, models,api


class Partner(models.Model):
    _inherit = "res.partner"

    display_delivery_address=fields.Boolean("Display Address",store=True)

    @api.onchange("display_delivery_address")
    def selection_change(self):
        for record in self:
            if record.display_delivery_address == True:
                record.type = 'delivery'
            else:
                record.type = 'contact'

    @api.onchange("type")
    def selection_ch(self):
        for record in self:
            if record.type == 'delivery':
                record.display_delivery_address = True
            else:
                record.display_delivery_address = False