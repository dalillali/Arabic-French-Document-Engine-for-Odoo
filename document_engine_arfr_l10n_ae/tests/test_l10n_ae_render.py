"""Functional render smoke test for UAE localization coexistence."""

from __future__ import annotations

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestL10nAeRenderSmoke(ArfrRenderCase):
    def test_uae_invoice_report_renders_with_arfr_engine(self):
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

        self.assertIn(self.partner.name, text)
        self.assertRegex(text, r"[٠١٢٣٤٥٦٧٨٩]")
