"""Functional render tests for bilingual invoice templates."""

from __future__ import annotations

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestBilingualTemplates(ArfrRenderCase):
    def test_arabic_french_invoice_report_renders_pdf(self):
        invoice = self.make_demo_invoice()

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )

        self.assertIn("ARFR Demo Customer", text)
        self.assertIn("Client", text)
        self.assertIn("Service conseil", text)

    def test_arabic_english_invoice_report_renders_pdf(self):
        invoice = self.make_demo_invoice()

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_en",
            invoice,
        )

        self.assertIn("ARFR Demo Customer", text)
        self.assertIn("Customer", text)
        self.assertIn("Service conseil", text)
