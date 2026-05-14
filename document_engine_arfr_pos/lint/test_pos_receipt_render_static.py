"""Static POS receipt rendering checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
POS = ROOT / "addons" / "document_engine_arfr_pos"


def test_receipt_patch_extends_order_receipt_without_replacement():
    js = (POS / "static" / "src" / "app" / "receipt" / "order_receipt_patch.js").read_text(encoding="utf-8")
    assert "patch(OrderReceipt.prototype" in js
    assert "arfrReceiptEnabled" in js
    assert "arfrReceiptDirection" in js
    assert "arfrFormatAmount" in js
    assert "class OrderReceipt" not in js


def test_receipt_formatter_formats_numerals_and_regional_currency():
    js = (POS / "static" / "src" / "app" / "arfr_format.js").read_text(encoding="utf-8")
    assert "ARABIC_INDIC_DIGITS" in js
    assert "REGIONAL_RULES" in js
    assert "arfrFormatNumerals" in js
    assert "arfrFormatAmount" in js
    assert "SAR" in js


def test_receipt_styles_are_scoped_to_opt_in_class():
    scss = (POS / "static" / "src" / "scss" / "pos_receipt_rtl.scss").read_text(encoding="utf-8")
    assert ".arfr-pos-receipt" in scss
    assert "unicode-bidi: isolate" in scss
    assert "white-space: nowrap" in scss


def test_receipt_template_extends_standard_receipt_root():
    xml = (POS / "static" / "src" / "xml" / "order_receipt.xml").read_text(encoding="utf-8")
    assert 't-inherit="point_of_sale.OrderReceipt"' in xml
    assert "arfrReceiptClass" in xml
    assert "arfrReceiptDirection" in xml
    assert "arfrFormatAmount" in xml
    assert "arfr-money" in xml


def test_receipt_tour_checks_arabic_indic_digits():
    js = (POS / "static" / "tests" / "tours" / "arfr_receipt_numerals_tour.js").read_text(encoding="utf-8")
    assert "arfr_pos_receipt_arabic_indic_digits" in js
    assert "arfr-pos-receipt" in js
    assert "١" in js


if __name__ == "__main__":
    test_receipt_patch_extends_order_receipt_without_replacement()
    test_receipt_formatter_formats_numerals_and_regional_currency()
    test_receipt_styles_are_scoped_to_opt_in_class()
    test_receipt_template_extends_standard_receipt_root()
    test_receipt_tour_checks_arabic_indic_digits()
