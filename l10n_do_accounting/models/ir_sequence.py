from odoo import models, fields


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    l10n_latam_journal_id = fields.One2many(
        "account.journal",
        string="Sequences",
    )

    expiration_date = fields.Date(
        string="NCF Expiration date",
        default=fields.Date.end_of(
            fields.Date.today().replace(year=fields.Date.today().year + 1), "year"
        ),
    )
    # TODO: Note for anyone from the future: use l10n_do prefix on v14, for God sake
