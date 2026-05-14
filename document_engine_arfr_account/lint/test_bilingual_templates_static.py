"""Static checks for bilingual invoice report templates."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
ACCOUNT = ROOT / "addons" / "document_engine_arfr_account"


def _read(name: str) -> str:
    path = ACCOUNT / "report" / name
    ET.parse(path)
    return path.read_text(encoding="utf-8")


def test_shared_bilingual_blocks_are_available():
    xml = _read("bilingual_blocks.xml")
    for template_id in [
        "arfr_report_shell",
        "arfr_bilingual_label_value",
        "arfr_bilingual_totals",
        "arfr_notes_block",
        "arfr_bilingual_signature",
    ]:
        assert f'id="{template_id}"' in xml
    assert "t-foreach" not in xml
    assert "document_engine_arfr_core.arfr_bilingual_document" in xml
    assert "paperformat_arfr_premium_document" in xml


def test_invoice_bilingual_actions_are_separate_from_standard_action():
    xml = _read("account_invoice_templates.xml")
    assert "report_invoice_document_arfr_direction" in xml
    assert "action_report_invoice_arfr_bilingual_ar_fr" in xml
    assert "action_report_invoice_arfr_bilingual_ar_en" in xml
    assert "report_invoice_arfr_bilingual" in xml
    assert "account.report_invoice" not in [
        "action_report_invoice_arfr_bilingual_ar_fr",
        "action_report_invoice_arfr_bilingual_ar_en",
    ]
    assert 'arfr_bilingual_pair">ar_fr<' in xml
    assert 'arfr_bilingual_pair">ar_en<' in xml
    assert xml.count("paperformat_arfr_premium_document") == 2


def test_invoice_bilingual_labels_are_structural_only():
    xml = _read("account_invoice_templates.xml")
    assert "document_engine_arfr_core.arfr_bilingual_document" in xml
    assert "arfr_bilingual_totals" in xml
    assert "arfr_bilingual_signature" in xml
    assert "arfr_secondary_lang" in xml
    assert "arfr_label('Customer'" in xml
    assert "_('Client')" not in xml


if __name__ == "__main__":
    test_shared_bilingual_blocks_are_available()
    test_invoice_bilingual_actions_are_separate_from_standard_action()
    test_invoice_bilingual_labels_are_structural_only()
