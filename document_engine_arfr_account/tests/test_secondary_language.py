"""Functional render tests for data-driven secondary language labels."""

from __future__ import annotations

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestSecondaryLanguage(ArfrRenderCase):
    def test_arabic_spanish_pair_uses_partner_secondary_language(self):
        self.partner.arfr_secondary_lang_id = self.ensure_language("es_ES")
        invoice = self.make_demo_invoice()

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )

        self.assertIn("Factura", text)
        self.assertIn("Cliente", text)

    def test_arabic_german_pair_uses_company_secondary_language(self):
        self.company.arfr_default_secondary_lang_id = self.ensure_language("de_DE")
        invoice = self.make_demo_invoice()

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_en",
            invoice,
        )

        self.assertIn("Rechnung", text)
        self.assertIn("Kunde", text)
