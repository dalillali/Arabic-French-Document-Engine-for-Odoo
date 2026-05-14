"""Static checks for numeral conversion helpers."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "addons" / "document_engine_arfr_core"))

from tools.numeral_format import (  # noqa: E402
    format_numerals,
    resolve_auto_numeral_system,
    to_arabic_indic,
    to_western,
)


def test_to_arabic_indic_converts_digits_and_preserves_punctuation():
    assert to_arabic_indic("SAR 1,234.56") == "SAR ١,٢٣٤.٥٦"


def test_to_western_converts_arabic_indic_digits():
    assert to_western("١٬٢٣٤٫٥٦ ر.س") == "1٬234٫56 ر.س"


def test_format_handles_negative_percent_and_dates():
    assert format_numerals("-12.5%", "arabic_indic") == "-١٢.٥%"
    assert format_numerals("2026-05-11", "arabic_indic") == "٢٠٢٦-٠٥-١١"


def test_format_preserves_mixed_identifier_letters():
    assert format_numerals("INV-2026-A7", "arabic_indic") == "INV-٢٠٢٦-A٧"


def test_decimal_is_not_scientific_notation():
    assert format_numerals(Decimal("1234.50"), "arabic_indic") == "١٢٣٤.٥٠"


def test_auto_policy_is_explicit_and_pinned():
    assert (
        resolve_auto_numeral_system(render_lang="ar_001", partner_lang="ar_001")
        == "arabic_indic"
    )
    assert resolve_auto_numeral_system(render_lang="ar_SA", partner_lang="ar") == "arabic_indic"
    assert resolve_auto_numeral_system(render_lang="fr_FR", partner_lang="ar") == "western"
    assert resolve_auto_numeral_system(render_lang="ar_001", partner_lang="fr_FR") == "western"
    assert format_numerals("123", "auto", render_lang="ar_001", partner_lang="ar") == "١٢٣"
    assert format_numerals("123", "auto", render_lang="fr_FR", partner_lang="ar") == "123"


if __name__ == "__main__":
    test_to_arabic_indic_converts_digits_and_preserves_punctuation()
    test_to_western_converts_arabic_indic_digits()
    test_format_handles_negative_percent_and_dates()
    test_format_preserves_mixed_identifier_letters()
    test_decimal_is_not_scientific_notation()
    test_auto_policy_is_explicit_and_pinned()
