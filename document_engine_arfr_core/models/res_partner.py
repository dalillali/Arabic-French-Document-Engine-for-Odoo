from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    arfr_numeral_system = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("western", "Western Arabic"),
            ("arabic_indic", "Arabic-Indic"),
            ("auto", "Automatic"),
        ],
        string="Document Numeral System",
        default="company",
        required=True,
        groups="base.group_user",
    )
    arfr_secondary_lang_id = fields.Many2one(
        comodel_name="res.lang",
        string="Document Secondary Language",
        groups="base.group_user",
    )
    arfr_bilingual_pair = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("none", "None"),
            ("ar_fr", "Arabic/French"),
            ("ar_en", "Arabic/English"),
        ],
        string="Document Bilingual Pair",
        default="company",
        required=True,
        groups="base.group_user",
    )
    arfr_currency_format_policy = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("odoo_default", "Odoo Default"),
            ("regional", "Regional"),
            ("force_western", "Force Western"),
        ],
        string="Document Currency Formatting",
        default="company",
        required=True,
        groups="base.group_user",
    )
