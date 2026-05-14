"""Static checks for numeral integration contracts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "addons" / "document_engine_arfr_core"
ACCOUNT = ROOT / "addons" / "document_engine_arfr_account"


def test_report_context_exposes_numeral_formatter():
    text = (CORE / "models" / "ir_actions_report.py").read_text(encoding="utf-8")
    assert "def arfr_format_numerals" in text
    assert "format_numerals" in text


def test_qweb_blocks_call_formatter_explicitly():
    xml = (ACCOUNT / "report" / "bilingual_blocks.xml").read_text(encoding="utf-8")
    assert "arfr_format_numerals" in xml
    assert "arfr_formatted_quantity" in xml
    assert "arfr_formatted_amount" in xml


if __name__ == "__main__":
    test_report_context_exposes_numeral_formatter()
    test_qweb_blocks_call_formatter_explicitly()
