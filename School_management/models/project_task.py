from odoo import fields, models


class InheritProject(models.Model):
    _inherit = "project.project"

    analytic_account_id = fields.Many2one("account.analytic.account")
    project_desc = fields.Char(
        string="Project", related="analytic_account_id.project_desc"
    )


class account(models.Model):
    _inherit = "account.analytic.account"

    project_desc = fields.Char(string="Project")


class InheritTask(models.Model):
    _inherit = "project.task"

    project_id = fields.Many2one("project.project")
    project_desc = fields.Char(string="Project", related="project_id.project_desc")
