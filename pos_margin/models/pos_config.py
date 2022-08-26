# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models, api, exceptions, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'


    journal_user = fields.Boolean('Use in Point of Sale',
        help="Check this box if this journal define a payment method that can be used in a point of sale.")


class PosConfig(models.Model):
    _inherit = "pos.config"

    iface_display_margin = fields.Boolean(
        string="Diplay Margin",
        help="Display Margin and Margin Rate in the frontend",
        default=True,
    )


    default_payment_method_id = fields.Many2one(
        comodel_name='account.journal',
        string='Default payment method',
        domain=[('journal_user', '=', True),
                ('type', 'in', ['bank', 'cash'])],
    )

    @api.constrains('journal_id', 'default_payment_method_id')
    def _check_default_payment_method_id(self):
        if not self.default_payment_method_id:
            return
        