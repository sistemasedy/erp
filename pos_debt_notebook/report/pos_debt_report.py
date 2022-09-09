# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017 Stanislav Krotov <https://it-projects.info/team/ufaks>
# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models, tools


class PosDebtReport(models.Model):

    _name = "report.pos.debt"
    _description = "POS Debt Statistics"
    _auto = False
    _order = "date desc"

    order_id = fields.Many2one("pos.order", string="POS Order", readonly=True)
    move_id = fields.Many2one("account.move", string="Invoice", readonly=True)
    payment_id = fields.Many2one("account.payment", string="Payment", readonly=True)
    update_id = fields.Many2one(
        "pos.credit.update", string="Manual Update", readonly=True
    )

    date = fields.Datetime(string="Date", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Partner", readonly=True)
    user_id = fields.Many2one("res.users", string="Salesperson", readonly=True)
    session_id = fields.Many2one("pos.session", string="Session", readonly=True)
    config_id = fields.Many2one("pos.config", string="POS", readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)
    currency_id = fields.Many2one("res.currency", string="Currency", readonly=True)
    journal_id = fields.Many2one("account.journal", string="Journals", readonly=True)

    state = fields.Selection(
        [("open", "Open"), ("confirm", "Validated")], readonly=True
    )
    credit_product = fields.Boolean(
        string="Journal Credit Product",
        help="Record is registered as Purchasing credit product",
        readonly=True,
    )
    balance = fields.Monetary(
        "Balance",
        help="Negative value for purchases without money (debt). Positive for credit payments (prepament or payments for debts).",
        readonly=True,
    )
    product_list = fields.Text("Product List", readonly=True)



