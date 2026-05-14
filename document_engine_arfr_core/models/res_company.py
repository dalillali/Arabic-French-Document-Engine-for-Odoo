from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    arfr_document_engine_enabled = fields.Boolean(
        string="Enable Arabic/French Document Engine",
        default=False,
        groups="base.group_system",
    )
    arfr_default_numeral_system = fields.Selection(
        selection=[
            ("western", "Western Arabic"),
            ("arabic_indic", "Arabic-Indic"),
            ("auto", "Automatic"),
        ],
        string="Default Numeral System",
        default="western",
        required=True,
        groups="base.group_system",
    )
    arfr_default_secondary_lang_id = fields.Many2one(
        comodel_name="res.lang",
        string="Default Secondary Language",
        groups="base.group_system",
    )
    arfr_default_bilingual_pair = fields.Selection(
        selection=[
            ("none", "None"),
            ("ar_fr", "Arabic/French"),
            ("ar_en", "Arabic/English"),
        ],
        string="Default Bilingual Pair",
        default="none",
        required=True,
        groups="base.group_system",
    )
    arfr_default_font_family = fields.Selection(
        selection=[
            ("noto", "Noto"),
            ("amiri", "Amiri"),
            ("system", "System Fonts"),
        ],
        string="Default Font Family",
        default="noto",
        required=True,
        groups="base.group_system",
    )
    arfr_currency_format_policy = fields.Selection(
        selection=[
            ("odoo_default", "Odoo Default"),
            ("regional", "Regional"),
            ("force_western", "Force Western"),
        ],
        string="Currency Formatting Policy",
        default="odoo_default",
        required=True,
        groups="base.group_system",
    )
    arfr_rtl_layout_policy = fields.Selection(
        selection=[
            ("auto", "Automatic"),
            ("force_ltr", "Force Left-to-Right"),
            ("force_rtl", "Force Right-to-Left"),
        ],
        string="RTL Layout Policy",
        default="auto",
        required=True,
        groups="base.group_system",
    )
    arfr_pos_receipt_enabled = fields.Boolean(
        string="Enable Arabic/French POS Receipts",
        default=False,
        groups="base.group_system",
    )
