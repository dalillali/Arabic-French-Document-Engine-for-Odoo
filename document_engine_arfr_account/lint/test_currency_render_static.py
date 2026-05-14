"""Static checks for opt-in currency rendering integration."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "addons" / "document_engine_arfr_core"
ACCOUNT = ROOT / "addons" / "document_engine_arfr_account"


def test_currency_asset_is_registered_after_rtl_asset():
    manifest = (CORE / "__manifest__.py").read_text(encoding="utf-8")
    assert "report_rtl.scss" in manifest
    assert "report_currency.scss" in manifest
    assert manifest.index("report_rtl.scss") < manifest.index("report_currency.scss")


def test_report_context_exposes_currency_helper():
    model = (CORE / "models" / "ir_actions_report.py").read_text(encoding="utf-8")
    assert "def arfr_format_currency" in model
    assert "format_currency(" in model


def test_bilingual_amounts_call_currency_helper_explicitly():
    blocks = (ACCOUNT / "report" / "bilingual_blocks.xml").read_text(encoding="utf-8")
    invoice = (ACCOUNT / "report" / "account_invoice_templates.xml").read_text(encoding="utf-8")
    assert "arfr_format_currency" in blocks
    assert "arfr-money" in blocks
    assert "currency_id" in invoice


def test_currency_scss_prevents_symbol_detachment():
    scss = (CORE / "static" / "src" / "scss" / "report_currency.scss").read_text(encoding="utf-8")
    assert ".arfr-money" in scss
    assert "white-space: nowrap" in scss
    assert "unicode-bidi: isolate" in scss


if __name__ == "__main__":
    test_currency_asset_is_registered_after_rtl_asset()
    test_report_context_exposes_currency_helper()
    test_bilingual_amounts_call_currency_helper_explicitly()
    test_currency_scss_prevents_symbol_detachment()
