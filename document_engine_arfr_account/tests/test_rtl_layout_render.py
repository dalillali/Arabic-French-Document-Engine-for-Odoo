"""Functional render tests for direction-aware account reports."""

from __future__ import annotations

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestRtlLayoutRender(ArfrRenderCase):
    def test_mixed_script_invoice_renders_without_missing_glyphs(self):
        invoice = self.make_demo_invoice(
            narration="ملاحظات بالعربية مع note francaise",
        )

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )

        self.assertIn("ARFR Demo Customer", text)
        self.assertIn("note francaise", text)

