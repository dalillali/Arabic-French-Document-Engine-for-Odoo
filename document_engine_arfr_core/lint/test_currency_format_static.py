"""Static checks for data-driven regional currency formatting helpers."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.currency_format import format_currency  # noqa: E402


@dataclass(frozen=True)
class Currency:
    name: str
    symbol: str
    position: str = "before"


def _seed_rules():
    rules = {}
    xml_path = ROOT / "data" / "arfr_currency_format_rules.xml"
    tree = ET.parse(xml_path)
    for record in tree.findall(".//record[@model='arfr.currency.format.rule']"):
        values = {}
        for field in record.findall("field"):
            values[field.attrib["name"]] = " " if field.attrib.get("eval") == "' '" else field.text or ""
        rules[values["currency_code"]] = {
            "symbol": values["symbol"],
            "position": values["position"],
            "thousands": values["thousands_separator"],
            "decimal": values["decimal_separator"],
        }
    return rules


RULES = _seed_rules()


def test_regional_rules_are_seeded_data_not_python_constants():
    source = (ROOT / "tools" / "currency_format.py").read_text(encoding="utf-8")
    assert "REGIONAL_RULES" not in source
    for currency_code in {"SAR", "AED", "MAD", "EGP", "EUR", "KWD", "QAR", "OMR", "BHD", "TND", "DZD", "IQD", "JOD", "LBP"}:
        assert currency_code in RULES


def test_regional_sar_arabic_indic():
    value = format_currency(
        1234.56,
        Currency("SAR", "ر.س"),
        numeral_system="arabic_indic",
        policy="regional",
        rules=RULES,
    )
    assert value == "١٬٢٣٤٫٥٦ ر.س"


def test_regional_mad_western():
    value = format_currency(
        1234.56,
        Currency("MAD", "MAD"),
        numeral_system="western",
        policy="regional",
        rules=RULES,
    )
    assert value == "1 234,56 MAD"


def test_regional_egp_negative_arabic_indic():
    value = format_currency(
        -42.5,
        Currency("EGP", "ج.م"),
        numeral_system="arabic_indic",
        policy="regional",
        rules=RULES,
    )
    assert value == "-٤٢٫٥٠ ج.م"


def test_eur_regional_western():
    value = format_currency(
        1234.56,
        Currency("EUR", "€"),
        numeral_system="western",
        policy="regional",
        rules=RULES,
    )
    assert value == "1 234,56 €"


def test_force_western_overrides_numeral_choice():
    value = format_currency(
        1234.56,
        Currency("SAR", "ر.س"),
        numeral_system="arabic_indic",
        policy="force_western",
        rules=RULES,
    )
    assert value == "ر.س 1,234.56"


if __name__ == "__main__":
    test_regional_rules_are_seeded_data_not_python_constants()
    test_regional_sar_arabic_indic()
    test_regional_mad_western()
    test_regional_egp_negative_arabic_indic()
    test_eur_regional_western()
    test_force_western_overrides_numeral_choice()
