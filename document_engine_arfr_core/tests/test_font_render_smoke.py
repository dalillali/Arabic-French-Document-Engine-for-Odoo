"""Functional smoke tests for the bundled font report."""

from __future__ import annotations

from .common import ArfrRenderCase


class TestFontRenderSmoke(ArfrRenderCase):
    def test_smoke_report_renders_pdf_without_tofu(self):
        text = self.render_report_text(
            "document_engine_arfr_core.action_report_arfr_font_smoke",
            self.company,
        )

        self.assertIn("Arabic/French Document Engine Font Smoke", text)
        self.assertIn("Facture de test francaise", text)
        self.assertIn("1,234.56", text)

