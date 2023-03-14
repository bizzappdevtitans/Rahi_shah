from odoo import fields, models


class InheritDesc(models.Model):
    _inherit = "sale.order"

    description = fields.Char(string="Descirption")
    payment_mode = fields.Selection(
        [
            ("online", "Online"),
            ("cash", "Cash"),
        ]
    )

    delivery_desc = fields.Char(string="Delivery Descirption")

    invoice_desc = fields.Char(string="Invoice Descirption")

    project_desc = fields.Char(string="project Descirption")

    def _prepare_invoice(self):
        rec = super(InheritDesc, self)._prepare_invoice()
        rec["in_invoice_desc"] = self.invoice_desc
        return rec

    def _prepare_analytic_account_data(self, prefix=None):
        vals = super(InheritDesc, self)._prepare_analytic_account_data(prefix)
        vals["project_desc"] = self.project_desc
        return vals


class down(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(down, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        invoice_vals["in_invoice_desc"] = order.invoice_desc
        return invoice_vals

    # def _create_invoice(self, order, so_line, amount):
    #     invoice_vals = super(down, self)._create_invoice(order, so_line, amount)
    #     invoice_vals.write({"in_invoice_desc": order.invoice_desc})


class Inheritorderline(models.Model):
    _inherit = "sale.order.line"

    order_lines = fields.Char(string="Header")


class Inheritstock(models.Model):
    _inherit = "stock.picking"

    in_delivery_desc = fields.Char(string="Delivery Descirption")


class Inheritinvoice(models.Model):
    _inherit = "account.move"

    in_invoice_desc = fields.Char(string="Invoice Descirption")


class stock(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        vals = super(stock, self)._get_new_picking_values()
        in_delivery_desc = self.group_id.sale_id.delivery_desc
        vals["in_delivery_desc"] = (
            any(rule.propagate_carrier for rule in self.rule_id) and in_delivery_desc
        )
        return vals


class InheritProject(models.Model):
    _inherit = "project.project"

    analytic_account_id = fields.Many2one("account.analytic.account")
    project_desc = fields.Char(string="Project", related="analytic_account_id.project_desc")


class account(models.Model):
    _inherit = "account.analytic.account"

    project_desc = fields.Char(string="Project")

class InheritTask(models.Model):
    _inherit="project.task"

    project_id=fields.Many2one("project.project")
    project_desc = fields.Char(string="Project", related="project_id.project_desc")



