"""Static POS preference and asset checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
POS = ROOT / "addons" / "document_engine_arfr_pos"


def test_pos_preferences_default_to_disabled():
    model = (POS / "models" / "pos_config.py").read_text(encoding="utf-8")
    assert "arfr_receipt_enabled" in model
    assert "default=False" in model
    assert "arfr_receipt_numeral_system" in model
    assert "arfr_receipt_currency_policy" in model
    assert "_load_pos_data_read" in model
    assert "arfr_resolved_receipt_preferences" in model
    assert "action_pos_data_for_ui" in model


def test_pos_assets_are_registered_in_pos_bundle():
    manifest = (POS / "__manifest__.py").read_text(encoding="utf-8")
    assert "point_of_sale._assets_pos" in manifest
    assert "web.assets_tests" in manifest
    assert "arfr_format.js" in manifest
    assert "order_receipt_patch.js" in manifest
    assert "pos_receipt_rtl.scss" in manifest
    assert "static/tests/tours" in manifest


if __name__ == "__main__":
    test_pos_preferences_default_to_disabled()
    test_pos_assets_are_registered_in_pos_bundle()
