"""Functional render tests for currency formatting in opt-in reports."""

from __future__ import annotations

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestCurrencyRender(ArfrRenderCase):
    def test_invoice_totals_render_through_pdf_pipeline(self):
        self.company.write(
            {
                "arfr_document_engine_enabled": True,
                "arfr_default_numeral_system": "arabic_indic",
                "arfr_currency_format_policy": "regional",
            }
        )
        invoice = self.make_demo_invoice()

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )

        self.assertIn("Total", text)
        currency_tokens = {self.company.currency_id.name, self.company.currency_id.symbol}
        self.assertTrue(
            any(token and token in text for token in currency_tokens),
            f"Expected one of {currency_tokens!r} in rendered text: {text!r}",
        )
