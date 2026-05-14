from inspect import signature

from odoo import api, models

from ..tools.currency_format import format_currency
from ..tools.numeral_format import format_numerals, scoped_numeral_system
from ..tools.preference_resolver import resolve_preferences


class ArfrFormatter(models.AbstractModel):
    _name = "arfr.formatter"
    _description = "Arabic/French Formatting Service"

    def _report_for_record(self, record=None):
        report = self.env.context.get("arfr_report")
        if report:
            return report
        return self.env["ir.actions.report"]

    def _render_lang(self, record=None, partner=None):
        context_lang = self.env.context.get("lang")
        if context_lang and context_lang.startswith("ar"):
            return context_lang
        partner = partner or getattr(record, "partner_id", None)
        if getattr(partner, "lang", None):
            return partner.lang
        country = getattr(partner, "country_id", None) or getattr(self.env.company, "country_id", None)
        report = self._report_for_record(record)
        if hasattr(report, "_arfr_pick_arabic_locale"):
            return report._arfr_pick_arabic_locale(getattr(country, "code", None))
        return "ar_001"

    @api.model
    def regulatory_context(self, record=None):
        report = self._report_for_record(record)
        if record and hasattr(report, "_arfr_regulatory_context"):
            return report._arfr_regulatory_context(record)
        return {}

    @api.model
    def resolve(self, record=None, **overrides):
        partner = overrides.pop("partner", None) or getattr(record, "partner_id", None)
        report = overrides.pop("report", None) or self._report_for_record(record)
        if report and len(report) == 1 and hasattr(report, "arfr_resolve_preferences"):
            return report.arfr_resolve_preferences(
                partner=partner,
                print_selection=overrides or None,
                regulatory=self.regulatory_context(record),
            )
        return resolve_preferences(
            company=self.env.company,
            partner=partner,
            print_selection=overrides or None,
            regulatory=self.regulatory_context(record),
        )

    @api.model
    def format_numerals(self, value, record=None, **overrides):
        resolved = overrides.pop("resolved", None) or self.resolve(record, **overrides)
        partner = overrides.get("partner") or getattr(record, "partner_id", None)
        numeral_system = overrides.get("numeral_system")
        field_key = overrides.get("field_key")
        return format_numerals(
            value,
            scoped_numeral_system(
                numeral_system or resolved.numeral_system,
                field_key=field_key,
                identifier_numerals=resolved.identifier_numerals,
                scope=resolved.numeral_scope,
            ),
            render_lang=self._render_lang(record, partner),
            partner_lang=getattr(partner, "lang", None),
        )

    @api.model
    def format_currency(self, amount, currency, record=None, **overrides):
        resolved = overrides.pop("resolved", None) or self.resolve(record, **overrides)
        partner = overrides.get("partner") or getattr(record, "partner_id", None)
        numeral_system = overrides.get("numeral_system") or resolved.numeral_system
        field_key = overrides.get("field_key")
        return format_currency(
            amount,
            currency,
            numeral_system=scoped_numeral_system(
                numeral_system,
                field_key=field_key,
                identifier_numerals=resolved.identifier_numerals,
                scope=resolved.numeral_scope,
            ),
            policy=overrides.get("currency_format_policy") or resolved.currency_format_policy,
            render_lang=self._render_lang(record, partner),
            partner_lang=getattr(partner, "lang", None),
            env=self.env,
        )

    @api.model
    def public_signatures(self):
        return {
            name: str(signature(getattr(type(self), name)))
            for name in ("format_numerals", "format_currency", "resolve", "regulatory_context")
        }
