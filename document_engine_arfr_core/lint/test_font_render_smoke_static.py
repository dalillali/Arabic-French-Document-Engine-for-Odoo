"""Smoke checks for the font report template.

Full PDF rendering is exercised by Odoo's test runner. These checks keep the
template and asset contract valid without requiring a running database.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "addons" / "document_engine_arfr_core"


def test_smoke_report_template_contains_arabic_and_latin_samples():
    xml = (CORE / "views" / "report_smoke_views.xml").read_text(encoding="utf-8")
    assert "فاتورة اختبار عربية" in xml
    assert "Facture de test francaise" in xml
    assert "arfr-report-fonts" in xml


def test_smoke_report_is_loaded_by_manifest():
    manifest = (CORE / "__manifest__.py").read_text(encoding="utf-8")
    assert "views/report_smoke_views.xml" in manifest


if __name__ == "__main__":
    test_smoke_report_template_contains_arabic_and_latin_samples()
    test_smoke_report_is_loaded_by_manifest()
