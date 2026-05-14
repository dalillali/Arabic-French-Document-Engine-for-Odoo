from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    arfr_document_engine_enabled = fields.Boolean(
        related="company_id.arfr_document_engine_enabled",
        readonly=False,
    )
    arfr_default_numeral_system = fields.Selection(
        related="company_id.arfr_default_numeral_system",
        readonly=False,
    )
    arfr_default_secondary_lang_id = fields.Many2one(
        related="company_id.arfr_default_secondary_lang_id",
        readonly=False,
    )
    arfr_default_bilingual_pair = fields.Selection(
        related="company_id.arfr_default_bilingual_pair",
        readonly=False,
    )
    arfr_default_font_family = fields.Selection(
        related="company_id.arfr_default_font_family",
        readonly=False,
    )
    arfr_currency_format_policy = fields.Selection(
        related="company_id.arfr_currency_format_policy",
        readonly=False,
    )
    arfr_rtl_layout_policy = fields.Selection(
        related="company_id.arfr_rtl_layout_policy",
        readonly=False,
    )
    arfr_pos_receipt_enabled = fields.Boolean(
        related="company_id.arfr_pos_receipt_enabled",
        readonly=False,
    )
