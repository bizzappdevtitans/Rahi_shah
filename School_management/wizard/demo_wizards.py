from odoo import api, fields, models


class DemoWizard(models.TransientModel):
    _name = 'demo.wizard'
    _description = "Demo Wizard"

    demo_field = fields.Char(string="Demo")


