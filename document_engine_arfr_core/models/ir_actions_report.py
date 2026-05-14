from odoo import _, fields, models

from ..tools.preference_resolver import resolve_preferences


BILINGUAL_PAIR_LANG = {
    "ar_fr": "fr_FR",
    "ar_en": "en_US",
}

ARABIC_LOCALE_BY_COUNTRY = {
    "SA": "ar_SA",
    "AE": "ar_AE",
    "MA": "ar_MA",
    "EG": "ar_EG",
}


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    arfr_enabled = fields.Boolean(
        string="Enable Arabic/French Rendering",
        default=False,
    )
    arfr_numeral_system = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("western", "Western Arabic"),
            ("arabic_indic", "Arabic-Indic"),
            ("auto", "Automatic"),
        ],
        string="Arabic/French Numeral System",
        default="company",
        required=True,
    )
    arfr_bilingual_pair = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("none", "None"),
            ("ar_fr", "Arabic/French"),
            ("ar_en", "Arabic/English"),
        ],
        string="Arabic/French Bilingual Pair",
        default="company",
        required=True,
    )
    arfr_font_family = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("noto", "Noto"),
            ("amiri", "Amiri"),
            ("system", "System Fonts"),
        ],
        string="Arabic/French Font Family",
        default="company",
        required=True,
    )
    arfr_currency_format_policy = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("odoo_default", "Odoo Default"),
            ("regional", "Regional"),
            ("force_western", "Force Western"),
        ],
        string="Arabic/French Currency Formatting",
        default="company",
        required=True,
    )
    arfr_layout_direction = fields.Selection(
        selection=[
            ("company", "Use Company Default"),
            ("auto", "Automatic"),
            ("force_ltr", "Force Left-to-Right"),
            ("force_rtl", "Force Right-to-Left"),
        ],
        string="Arabic/French Layout Direction",
        default="company",
        required=True,
    )

    def arfr_resolve_preferences(self, partner=None, print_selection=None, regulatory=None):
        self.ensure_one()
        return resolve_preferences(
            company=self.env.company,
            report=self,
            partner=partner,
            print_selection=print_selection,
            regulatory=regulatory,
        )

    def _arfr_pick_arabic_locale(self, country_code=None):
        return ARABIC_LOCALE_BY_COUNTRY.get(country_code or "", "ar_001")

    def _arfr_regulatory_context(self, record):
        """Return regulatory rendering rules for ``record``."""

        return {}

    def _arfr_secondary_lang(self, record=None, partner=None, fallback=None):
        self.ensure_one()
        fallback = fallback or BILINGUAL_PAIR_LANG.get(self.arfr_bilingual_pair)
        resolved = self.arfr_resolve_preferences(
            partner=partner or getattr(record, "partner_id", None),
            print_selection={"secondary_lang": fallback} if fallback else None,
        )
        return resolved.secondary_lang or fallback

    def _arfr_label(self, source, secondary_lang=None, record=None):
        if not secondary_lang:
            return _(source)
        translator = (record or self).with_context(lang=secondary_lang)
        translated = translator.env._(source)
        if translated != source:
            return translated
        return self.env["arfr.label.dictionary"].sudo().translate_label(source, secondary_lang)

    def arfr_format_numerals(
        self,
        value,
        numeral_system=None,
        partner=None,
        field_key=None,
        record=None,
    ):
        self.ensure_one()
        return self.env["arfr.formatter"].with_context(arfr_report=self).format_numerals(
            value,
            record=record,
            partner=partner,
            numeral_system=numeral_system,
            field_key=field_key,
        )

    def arfr_format_currency(
        self,
        amount,
        currency,
        numeral_system=None,
        partner=None,
        field_key=None,
        record=None,
    ):
        self.ensure_one()
        return self.env["arfr.formatter"].with_context(arfr_report=self).format_currency(
            amount,
            currency,
            record=record,
            partner=partner,
            numeral_system=numeral_system,
            field_key=field_key,
        )

    def _get_rendering_context(self, report, docids, data):
        data = super()._get_rendering_context(report, docids, data)
        docs = data.get("docs")
        default_record = docs[:1] if docs else self.env[report.model].browse((docids or [])[:1])
        formatter = self.env["arfr.formatter"].with_context(arfr_report=report)
        resolved_cache = {}

        def _record_key(record):
            return (record._name, record.id) if record else (None, None)

        def _resolved(record=None, partner=None, fallback=None):
            record = record or default_record
            partner = partner or getattr(record, "partner_id", None)
            key = (_record_key(record), partner.id if partner else None, fallback)
            if key not in resolved_cache:
                resolved_cache[key] = formatter.resolve(
                    record,
                    partner=partner,
                    secondary_lang=fallback,
                )
            return resolved_cache[key]

        def arfr_format_numerals(value, numeral_system=None, partner=None, field_key=None, record=None):
            record = record or default_record
            return formatter.format_numerals(
                value,
                record=record,
                partner=partner,
                numeral_system=numeral_system,
                field_key=field_key,
                resolved=_resolved(record=record, partner=partner),
            )

        def arfr_format_currency(
            amount,
            currency,
            numeral_system=None,
            partner=None,
            field_key=None,
            record=None,
        ):
            record = record or default_record
            return formatter.format_currency(
                amount,
                currency,
                record=record,
                partner=partner,
                numeral_system=numeral_system,
                field_key=field_key,
                resolved=_resolved(record=record, partner=partner),
            )

        def arfr_secondary_lang(record=None, partner=None, fallback=None):
            fallback = fallback or BILINGUAL_PAIR_LANG.get(report.arfr_bilingual_pair)
            return _resolved(
                record=record or default_record,
                partner=partner,
                fallback=fallback,
            ).secondary_lang or fallback

        def arfr_label(source, secondary_lang=None, record=None):
            return report._arfr_label(
                source,
                secondary_lang=secondary_lang,
                record=record or default_record,
            )

        data["_"] = _
        data["arfr_formatter"] = formatter
        data["arfr_regulatory_context"] = formatter.regulatory_context(default_record)
        data["arfr_rendering_preferences"] = _resolved(default_record)
        data["arfr_secondary_lang"] = arfr_secondary_lang
        data["arfr_label"] = arfr_label
        data["arfr_format_numerals"] = arfr_format_numerals
        data["arfr_format_currency"] = arfr_format_currency
        return data
