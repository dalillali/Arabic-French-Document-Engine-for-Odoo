from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    arfr_receipt_enabled = fields.Boolean(
        string="Enable Arabic/French Receipt Rendering",
        default=False,
    )
    arfr_receipt_numeral_system = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("western", "Western Arabic"),
            ("arabic_indic", "Arabic-Indic"),
            ("auto", "Automatic"),
        ],
        string="Receipt Numeral System",
        default="company",
        required=True,
    )
    arfr_receipt_currency_policy = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("odoo_default", "Odoo Default"),
            ("regional", "Regional"),
            ("force_western", "Force Western"),
        ],
        string="Receipt Currency Formatting",
        default="company",
        required=True,
    )
    arfr_receipt_layout_direction = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("auto", "Automatic"),
            ("force_ltr", "Force Left-to-Right"),
            ("force_rtl", "Force Right-to-Left"),
        ],
        string="Receipt Layout Direction",
        default="company",
        required=True,
    )

    def _arfr_resolved_receipt_preferences(self):
        self.ensure_one()
        company = self.company_id
        return {
            "enabled": bool(
                self.arfr_receipt_enabled or company.arfr_pos_receipt_enabled
            ),
            "numeral_system": self._arfr_first_explicit(
                self.arfr_receipt_numeral_system,
                company.arfr_default_numeral_system,
            ),
            "currency_format_policy": self._arfr_first_explicit(
                self.arfr_receipt_currency_policy,
                company.arfr_currency_format_policy,
            ),
            "layout_direction": self._arfr_first_explicit(
                self.arfr_receipt_layout_direction,
                company.arfr_rtl_layout_policy,
            ),
        }

    def _arfr_first_explicit(self, value, fallback):
        return fallback if value in (None, "", "company") else value

    def _load_pos_data_read(self, records, config):
        read_records = super()._load_pos_data_read(records, config)
        for record in read_records:
            if record.get("id") == config.id:
                record["arfr_receipt_enabled"] = config.arfr_receipt_enabled
                record["arfr_receipt_numeral_system"] = config.arfr_receipt_numeral_system
                record["arfr_receipt_currency_policy"] = config.arfr_receipt_currency_policy
                record["arfr_receipt_layout_direction"] = config.arfr_receipt_layout_direction
                record["arfr_resolved_receipt_preferences"] = (
                    config._arfr_resolved_receipt_preferences()
                )
        return read_records

    def action_pos_data_for_ui(self):
        parent = getattr(super(), "action_pos_data_for_ui", None)
        data = parent() if parent else {}
        if isinstance(data, dict):
            data["arfr_resolved_receipt_preferences"] = (
                self._arfr_resolved_receipt_preferences()
            )
        return data
