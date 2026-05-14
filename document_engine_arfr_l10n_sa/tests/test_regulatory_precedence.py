"""Functional tests for Saudi regulatory numeral precedence."""

from __future__ import annotations

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestSaudiRegulatoryPrecedence(ArfrRenderCase):
    def test_saudi_identifier_scope_keeps_invoice_number_western(self):
        self.company.write(
            {
                "arfr_document_engine_enabled": True,
                "arfr_default_numeral_system": "arabic_indic",
                "arfr_currency_format_policy": "regional",
            }
        )
        invoice = self.make_demo_invoice()
        invoice.write({"name": "INV/2026/0007"})

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )

        self.assertIn("INV/2026/0007", text)
        self.assertNotIn("INV/٢٠٢٦/٠٠٠٧", text)
        self.assertRegex(text, r"[٠١٢٣٤٥٦٧٨٩]")
