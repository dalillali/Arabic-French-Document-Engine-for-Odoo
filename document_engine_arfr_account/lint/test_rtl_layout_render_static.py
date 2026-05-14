"""Static checks for RTL report template inheritance."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "addons" / "document_engine_arfr_core"
ACCOUNT = ROOT / "addons" / "document_engine_arfr_account"


def test_rtl_asset_is_registered():
    manifest = (CORE / "__manifest__.py").read_text(encoding="utf-8")
    assert "report_rtl.scss" in manifest


def test_report_layout_extends_web_report_layout():
    xml = (CORE / "views" / "report_layout_views.xml").read_text(encoding="utf-8")
    assert 'inherit_id="web.report_layout"' in xml
    assert "arfr-report-root" in xml


def test_business_document_templates_use_xpath_inheritance():
    templates = {
        "account_invoice_templates.xml": "account.report_invoice_document",
        "sale_order_templates.xml": "sale.report_saleorder_document",
        "purchase_order_templates.xml": "purchase.report_purchaseorder_document",
        "stock_delivery_templates.xml": "stock.report_delivery_document",
    }
    for file_name, inherit_id in templates.items():
        xml = (ACCOUNT / "report" / file_name).read_text(encoding="utf-8")
        assert f'inherit_id="{inherit_id}"' in xml
        assert "<xpath" in xml
        assert "arfr-direction-aware" in xml


def test_rtl_scss_is_scoped_to_arfr_classes():
    scss = (CORE / "static" / "src" / "scss" / "report_rtl.scss").read_text(
        encoding="utf-8"
    )
    assert ".arfr-report-root" in scss
    assert ".arfr-table" in scss
    assert "unicode-bidi: isolate" in scss


if __name__ == "__main__":
    test_rtl_asset_is_registered()
    test_report_layout_extends_web_report_layout()
    test_business_document_templates_use_xpath_inheritance()
    test_rtl_scss_is_scoped_to_arfr_classes()
