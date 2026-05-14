"""Static checks for bilingual quotation report templates."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / "addons" / "document_engine_arfr_account" / "report" / "sale_order_templates.xml"


def test_bilingual_quotation_actions_are_selectable_variants():
    ET.parse(REPORT)
    xml = REPORT.read_text(encoding="utf-8")
    assert "action_report_saleorder_arfr_bilingual_ar_fr" in xml
    assert "action_report_saleorder_arfr_bilingual_ar_en" in xml
    assert "sale.report_saleorder_document" in xml
    assert 'binding_model_id" ref="sale.model_sale_order"' in xml


def test_bilingual_quotation_structural_sections_exist():
    xml = REPORT.read_text(encoding="utf-8")
    assert "document_engine_arfr_core.arfr_bilingual_document" in xml
    assert "Quotation" in xml
    assert "Arabic / French" in xml
    assert "Arabic / English" in xml


if __name__ == "__main__":
    test_bilingual_quotation_actions_are_selectable_variants()
    test_bilingual_quotation_structural_sections_exist()
