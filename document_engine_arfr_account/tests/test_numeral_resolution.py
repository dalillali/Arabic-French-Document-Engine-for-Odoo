"""Functional render tests for numeral preference resolution."""

from __future__ import annotations

from odoo.tests import tagged

from odoo.addons.document_engine_arfr_core.tests.common import ArfrRenderCase


@tagged("post_install", "-at_install")
class TestNumeralResolution(ArfrRenderCase):
    def test_partner_preference_is_visible_in_rendered_invoice(self):
        self.company.write(
            {
                "arfr_document_engine_enabled": True,
                "arfr_default_numeral_system": "western",
            }
        )
        self.partner.write({"arfr_numeral_system": "arabic_indic"})
        invoice = self.make_demo_invoice()

        text = self.render_report_text(
            "document_engine_arfr_account.action_report_invoice_arfr_bilingual_ar_fr",
            invoice,
        )

        self.assertRegex(text, r"[٠١٢٣٤٥٦٧٨٩]")

