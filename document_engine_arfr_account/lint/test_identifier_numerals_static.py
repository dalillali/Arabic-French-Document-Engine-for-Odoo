"""Document identifier numeral safety checks."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "addons" / "document_engine_arfr_core"))

from tools.preference_resolver import resolve_preferences  # noqa: E402
from tools.numeral_format import format_numerals  # noqa: E402


def test_identifiers_are_only_converted_when_helper_is_explicitly_called():
    invoice_number = "INV/2026/0007"
    assert invoice_number == "INV/2026/0007"
    assert format_numerals(invoice_number, "arabic_indic") == "INV/٢٠٢٦/٠٠٠٧"


def test_regulatory_policy_can_force_numeral_context():
    resolved = resolve_preferences(
        company={"arfr_document_engine_enabled": True, "arfr_default_numeral_system": "western"},
        regulatory={"enabled": True, "numeral_system": "arabic_indic"},
    )
    assert resolved.numeral_system == "arabic_indic"


if __name__ == "__main__":
    test_identifiers_are_only_converted_when_helper_is_explicitly_called()
    test_regulatory_policy_can_force_numeral_context()
