"""Static install-safety checks for configuration defaults and views."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "addons" / "document_engine_arfr_core"
POS = ROOT / "addons" / "document_engine_arfr_pos"


def test_company_defaults_keep_engine_disabled():
    text = (CORE / "models" / "res_company.py").read_text(encoding="utf-8")
    assert "arfr_document_engine_enabled" in text
    assert "default=False" in text
    assert 'default="western"' in text
    assert 'default="none"' in text


def test_views_extend_existing_odoo_views():
    for view_file in (
        CORE / "views" / "res_config_settings_views.xml",
        CORE / "views" / "res_partner_views.xml",
        CORE / "views" / "ir_actions_report_views.xml",
        POS / "views" / "pos_config_views.xml",
    ):
        xml = view_file.read_text(encoding="utf-8")
        assert "inherit_id" in xml
        assert "<xpath" in xml


def test_pos_defaults_keep_receipt_disabled():
    text = (POS / "models" / "pos_config.py").read_text(encoding="utf-8")
    assert "arfr_receipt_enabled" in text
    assert "default=False" in text


if __name__ == "__main__":
    test_company_defaults_keep_engine_disabled()
    test_views_extend_existing_odoo_views()
    test_pos_defaults_keep_receipt_disabled()
