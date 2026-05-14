"""Backward-compatibility checks for standard report preservation."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "addons" / "document_engine_arfr_account" / "report"


def test_templates_use_inheritance_or_new_actions_only():
    for path in REPORT_DIR.glob("*.xml"):
        ET.parse(path)
        xml = path.read_text(encoding="utf-8")
        assert "<delete" not in xml
        assert "position=\"replace\"" not in xml
        if path.name != "bilingual_blocks.xml":
            assert "inherit_id=" in xml or "model=\"ir.actions.report\"" in xml


def test_standard_report_actions_are_not_redefined():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in REPORT_DIR.glob("*.xml"))
    forbidden_record_ids = [
        'id="account.account_invoices"',
        'id="sale.action_report_saleorder"',
        'id="purchase.action_report_purchase_order"',
        'id="stock.action_report_delivery"',
    ]
    for record_id in forbidden_record_ids:
        assert record_id not in combined


def test_bilingual_purchase_and_delivery_variants_exist():
    purchase = (REPORT_DIR / "purchase_order_templates.xml").read_text(encoding="utf-8")
    delivery = (REPORT_DIR / "stock_delivery_templates.xml").read_text(encoding="utf-8")
    assert "action_report_purchaseorder_arfr_bilingual_ar_fr" in purchase
    assert "action_report_purchaseorder_arfr_bilingual_ar_en" in purchase
    assert "action_report_delivery_arfr_bilingual_ar_fr" in delivery
    assert "action_report_delivery_arfr_bilingual_ar_en" in delivery


if __name__ == "__main__":
    test_templates_use_inheritance_or_new_actions_only()
    test_standard_report_actions_are_not_redefined()
    test_bilingual_purchase_and_delivery_variants_exist()
