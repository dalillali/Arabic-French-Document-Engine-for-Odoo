"""Unit tests for rendering preference resolution."""

from __future__ import annotations

from dataclasses import dataclass

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "addons" / "document_engine_arfr_core"))

from tools.preference_resolver import resolve_preferences  # noqa: E402


@dataclass
class Obj:
    arfr_document_engine_enabled: bool = False
    arfr_default_numeral_system: str = "western"
    arfr_default_bilingual_pair: str = "none"
    arfr_default_secondary_lang_id: object | None = None
    arfr_default_font_family: str = "noto"
    arfr_currency_format_policy: str = "odoo_default"
    arfr_rtl_layout_policy: str = "auto"
    arfr_enabled: bool = False
    arfr_numeral_system: str = "company"
    arfr_bilingual_pair: str = "company"
    arfr_font_family: str = "company"
    arfr_layout_direction: str = "company"
    arfr_secondary_lang_id: object | None = None


@dataclass
class Lang:
    code: str


def test_defaults_are_odoo_standard_when_disabled():
    resolved = resolve_preferences(company=Obj())
    assert resolved.enabled is False
    assert resolved.numeral_system == "western"
    assert resolved.bilingual_pair == "none"


def test_partner_overrides_company_for_numerals():
    company = Obj(arfr_document_engine_enabled=True, arfr_default_numeral_system="western")
    partner = {"arfr_numeral_system": "arabic_indic"}
    resolved = resolve_preferences(company=company, partner=partner)
    assert resolved.enabled is True
    assert resolved.numeral_system == "arabic_indic"


def test_report_overrides_partner_for_numerals():
    company = Obj(arfr_document_engine_enabled=True, arfr_default_numeral_system="western")
    partner = {"arfr_numeral_system": "arabic_indic"}
    report = Obj(arfr_enabled=True, arfr_numeral_system="western")
    resolved = resolve_preferences(company=company, partner=partner, report=report)
    assert resolved.numeral_system == "western"


def test_secondary_language_resolves_partner_then_company():
    company = Obj(arfr_default_secondary_lang_id=Lang("de_DE"))
    partner = Obj(arfr_secondary_lang_id=Lang("es_ES"))

    resolved = resolve_preferences(company=company, partner=partner)

    assert resolved.secondary_lang == "es_ES"
    assert resolve_preferences(company=company).secondary_lang == "de_DE"


def test_regulatory_overrides_everything():
    company = Obj(arfr_document_engine_enabled=True, arfr_default_numeral_system="western")
    report = Obj(arfr_enabled=True, arfr_numeral_system="western")
    partner = {"arfr_numeral_system": "western"}
    regulatory = {"enabled": True, "numeral_system": "arabic_indic"}
    resolved = resolve_preferences(
        company=company,
        report=report,
        partner=partner,
        regulatory=regulatory,
    )
    assert resolved.enabled is True
    assert resolved.numeral_system == "arabic_indic"


if __name__ == "__main__":
    test_defaults_are_odoo_standard_when_disabled()
    test_partner_overrides_company_for_numerals()
    test_report_overrides_partner_for_numerals()
    test_secondary_language_resolves_partner_then_company()
    test_regulatory_overrides_everything()
