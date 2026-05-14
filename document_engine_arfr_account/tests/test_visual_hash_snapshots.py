"""Perceptual hash regression checks for rendered PDFs."""

from __future__ import annotations

from pathlib import Path

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


FIXTURES = Path(__file__).parent / "fixtures" / "golden"

try:
    import imagehash
    from pdf2image import convert_from_bytes
except ImportError:  # pragma: no cover - exercised only in the Odoo test env
    imagehash = None
    convert_from_bytes = None


@tagged("post_install", "-at_install")
class TestVisualHashSnapshots(ArfrRenderCase):
    def setUp(self):
        super().setUp()
        self.company.write(
            {
                "arfr_document_engine_enabled": True,
                "arfr_default_numeral_system": "arabic_indic",
                "arfr_currency_format_policy": "regional",
            }
        )

    def _assert_phash(self, name, pdf_bytes):
        if imagehash is None or convert_from_bytes is None:
            self.skipTest("pdf2image and imagehash are required for visual regression tests")

        fixture = FIXTURES / f"{name}.phash"
        expected_text = fixture.read_text(encoding="utf-8").strip()
        self.assertRegex(expected_text, r"^[0-9a-fA-F]{16}$")
        page = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)[0]
        actual = imagehash.phash(page)
        expected = imagehash.hex_to_hash(expected_text)

        # Hamming distance <= 8 tolerates antialiasing/render backend noise while catching layout drift.
        self.assertLessEqual(actual - expected, 8, f"{name} visual hash changed: expected {expected}, got {actual}")

    def test_invoice_visual_hash_stays_close_to_golden(self):
        invoice = self.make_demo_invoice()
        pdf_bytes = self.render_report_pdf(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )
        self._assert_phash("invoice_ar_fr", pdf_bytes)
